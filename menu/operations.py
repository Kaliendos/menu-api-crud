from typing import List
from uuid import UUID

from sqlalchemy import func

from . import models, schemas
from .base_classes import BaseOperation


class MenuOperations(BaseOperation):

    def _get_menu(self, menu_id):
        return self.get_object_or_404(models.Menu, menu_id, "menu not found")

    def get_menu_list(self) -> List[models.Menu]:
        menu_list = self.get_objects_list(models.Menu)
        submenus_count_list = (
            self.session.query(models.Menu, func.count(models.SubMenu.id))
                .where(models.SubMenu.menu_id == models.Menu.id)
                .group_by(models.Menu.id).all()
        )
        dishes_count = (
            self.session.query(models.Menu, func.count(models.SubMenu.Dish))
                .filter(models.SubMenu.menu_id == models.Menu.id)
                .group_by(models.Menu.id).all()
        )
        for menu, count in submenus_count_list:
            menu.submenus_count = count
        for menu, count in dishes_count:
            menu.dishes_count = count
        return menu_list

    def get_menu_by_id(self, menu_id) -> models.Menu:
        menu = self._get_menu(menu_id)
        submenus = menu.sub_menu.all()
        menu.submenus_count = len(submenus)
        dishes_count = 0
        for submenu in submenus:
            for _ in submenu.Dish:
                dishes_count += 1
        menu.dishes_count = dishes_count
        return menu

    def create_menu(self, request_data: schemas.PostMenuSchema) -> models.Menu:
        menu_obj = models.Menu(**request_data.dict())
        self.session.add(menu_obj)
        self.session.commit()
        return menu_obj

    def patch_menu(self, menu_id: UUID,
                   schema: schemas.PatchMenuSchema) -> models.Menu:
        menu = self._get_menu(menu_id)
        data_dict = schema.dict(exclude_unset=True)
        for field, value in data_dict.items():
            setattr(menu, field, value)
        self.session.commit()
        return menu

    def delete_menu(self, menu_id: UUID):
        self.session.delete(self.get_menu_by_id(menu_id))
        self.session.commit()


class SubMenuOperations(BaseOperation):

    def _get_submenu(self, submenu_id):
        return self.get_object_or_404(
            models.SubMenu, submenu_id, "submenu not found"
        )

    def get_sub_menu_list(self, menu_id) -> List[models.SubMenu]:
        menu = self.get_object_or_404(models.Menu, menu_id, "menu not found")
        for submenu in menu.sub_menu.all():
            for dish in submenu.Dish:
                submenu.submenus_count = dish
        return menu.sub_menu.all()

    def create_submenu(
            self, menu_id,
            request_data: schemas.CreateSubMenuSchema) -> models.SubMenu:
        submenu_instance = models.SubMenu(**request_data.dict())
        submenu_instance.menu_id = menu_id
        self.session.add(submenu_instance)
        self.session.commit()
        return submenu_instance

    def get_submenu_by_id(self, submenu_id) -> schemas.GetSubMenuSchema:
        submenu = self._get_submenu(submenu_id)
        submenu.dishes_count = len(submenu.Dish.all())
        return submenu

    def patch_submenu(self, submenu_id, schema: schemas.PatchMenuSchema):
        submenu = self._get_submenu(submenu_id)
        data_dict = schema.dict(exclude_unset=True)
        for field, value in data_dict.items():
            setattr(submenu, field, value)
        self.session.commit()
        return submenu

    def delete_submenu(self, submenu_id):
        self.session.delete(self._get_submenu(submenu_id))
        self.session.commit()


class DishOperation(BaseOperation):

    def _get_dish(self, dish_id):
        return self.get_object_or_404(models.Dish, dish_id, "dish not found")

    def create_dish(
            self, submenu_id,
            request_data: schemas.DishSchema) -> models.Dish:
        dish_obj = models.Dish(**request_data.dict())
        dish_obj.sub_menu_id = submenu_id
        self.session.add(dish_obj)
        self.session.commit()
        return dish_obj

    def get_dish_list(self, sub_menu) -> List[models.Dish]:
        return (
            self.session.query(models.Dish)
            .filter(models.Dish.sub_menu_id == sub_menu)
            .all()
        )

    def get_dish_item(self, dish_id) -> models.Dish:
        return self._get_dish(dish_id)

    def patch_dish(
            self, dish_id,
            schema: schemas.UpdateDishSchema) -> models.Dish:
        dish = self._get_dish(dish_id)
        data_dict = schema.dict(exclude_unset=True)
        for field, value in data_dict.items():
            setattr(dish, field, value)
        self.session.commit()
        return dish

    def delete_dish(self, dish_id):
        self.session.delete(self._get_dish(dish_id))
        self.session.commit()
