from typing import List
from uuid import UUID

from fastapi import Depends, HTTPException, Request, Body
from sqlalchemy import func, update

from config.database.db import SessionLocal, get_session
from . import models, schemas



class AbstractOperation:
    def __init__(self, session: SessionLocal = Depends(get_session)):
        self.session = session

    def get_objects_list(self, model):
        """Получить список объектов, принимает параметр model в качестве модели"""
        return (
            self.session
            .query(model)
            .all()
        )

    def get_object_or_404(self, model, object_id):
        obj_instance = self.session.query(model).get(object_id)
        if obj_instance is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return obj_instance


class MenuOperations(AbstractOperation):

    def calc_submenus_count(self, obj_id=None) -> int | List[tuple]:
        """
        Подсчитывает количиество связаных подменю для models.Menu, если передан параметр
        obj_id, то будет возвращено количество типа int, иначе список кортежей
         """
        if obj_id:
            menu_item = (
                self.session.query(models.Menu)
                .filter(models.Menu.id == obj_id)
                .subquery()
            )
            submenus_count_for_object = (
                self.session.query(
                    menu_item.c.id, func.count(models.SubMenu.id)
                ).outerjoin(models.SubMenu).group_by(menu_item.c.id).all()[0][1])
            return submenus_count_for_object

        submenus_count_for_list = (
            self.session.query(models.Menu, func.count(models.SubMenu.id))
                .outerjoin(models.SubMenu).group_by(models.Menu.id).all())
        return submenus_count_for_list

    def get_menu_list(self) -> List[models.Menu]:
        menu_list = self.get_objects_list(models.Menu)
        for menu, submenus_count in self.calc_submenus_count():
            menu.submenus_count = submenus_count
        return menu_list

    def get_menu_by_id(self, menu_id) -> models.Menu:
        menu = self.get_object_or_404(models.Menu, menu_id)
        menu.submenus_count = self.calc_submenus_count(menu_id)
        return menu

    def create_menu(self, request_data: schemas.PostMenuSchema) -> models.Menu:
        menu_obj = models.Menu(**request_data.dict())
        self.session.add(menu_obj)
        self.session.commit()
        return menu_obj

    def patch_menu(self, menu_id: UUID, schema: schemas.PatchMenuSchema) -> models.Menu:
        menu = self.session.query(models.Menu).filter_by(id=menu_id).first()
        data_dict = schema.dict(exclude_unset=True)
        for field, value in data_dict.items():
            setattr(menu, field, value)
        self.session.commit()
        return menu

    def delete_menu(self, menu_id: UUID):
        self.session.delete(self.get_menu_by_id(menu_id))
        self.session.commit()


class SubMenuOperations(AbstractOperation):

    def get_sub_menu_list(self, menu_id) -> List[models.SubMenu]:
        menu = self.get_object_or_404(models.Menu,menu_id)
        return menu.sub_menu.all()

    def create_submenu(self, menu_id, request_data: schemas.CreateSubMenuSchema) -> models.SubMenu:
        submenu_instance = models.SubMenu(**request_data.dict())
        submenu_instance.menu_id = menu_id
        self.session.add(submenu_instance)
        self.session.commit()
        return submenu_instance

    def get_submenu_by_id(self, submenu_id) -> schemas.GetSubMenuSchema:
        submenu = self.get_object_or_404(models.SubMenu, submenu_id)
        return submenu

    def patch_submenu(self, submenu_id, schema: schemas.PatchMenuSchema):
        submenu = self.get_object_or_404(models.SubMenu, submenu_id)
        data_dict = schema.dict(exclude_unset=True)
        for field, value in data_dict.items():
            setattr(submenu, field, value)
        self.session.commit()
        return submenu

    def delete_submenu(self, submenu_id):
        self.session.delete(self.get_submenu_by_id(submenu_id))
        self.session.commit()


class DishOperation(AbstractOperation):

    def create_dish(self, submenu_id, request_data: schemas.DishSchema) -> models.Dish:
        dish_obj = models.Dish(**request_data.dict())
        dish_obj.sub_menu_id = submenu_id
        self.session.add(dish_obj)
        self.session.commit()
        return dish_obj

    def get_dish_list(self, sub_menu):
        return (
            self.session.query(models.Dish)
            .filter(models.Dish.sub_menu_id == sub_menu)
            .all()
        )

    def get_dish_item(self, sub_menu_id, dish_id) -> models.Dish:
        submenu = self.get_object_or_404(models.SubMenu, sub_menu_id)
        dish = submenu.Dish.filter(models.Dish.id == dish_id).first()
        if dish is None:
            raise HTTPException(status_code=404)
        return dish




