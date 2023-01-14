from typing import List

from fastapi import Depends

from config.database.db import SessionLocal, get_session
from . import models, schemas
from .schemas import  CreateMenuSchema


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


class MenuOperations(AbstractOperation):

    def get_menu_list(self) -> List[models.Menu]:
        return self.get_objects_list(models.Menu)

    def get_menu_by_id(self, menu_id) -> models.Menu:
        menu_instance = self.session.query(models.Menu).get(menu_id)
        return menu_instance

    def create_menu(self, request_data: CreateMenuSchema) -> models.Menu:
        menu_instance = models.Menu(**request_data.dict())
        self.session.add(menu_instance)
        self.session.commit()
        return menu_instance


class SubMenuOperations(AbstractOperation):

    def get_menu_list(self) -> List[models.SubMenu]:
        return self.get_objects_list(models.SubMenu)

    def create_submenu(self,menu_id, request_data: schemas.CreateSubMenuSchema) -> models.SubMenu:
        submenu_instance = models.SubMenu(**request_data.dict())
        submenu_instance.menu_id = menu_id
        self.session.add(submenu_instance)
        self.session.commit()
        return submenu_instance



