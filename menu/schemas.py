from uuid import UUID

from pydantic import BaseModel


class AbstractMenuShema(BaseModel):
    """Абстрактный класс для операций меню"""
    title: str
    description: str

    class Config:
        orm_mode = True


class AbsractSubMenuSchema(BaseModel):
    """Абстрактный класс для операций SubMenu"""
    title: str
    description: str

    class Config:
        orm_mode = True


class GetMenuSchema(AbstractMenuShema):
    """Получение меню"""
    id: UUID
    submenus_count: int = 0
    dishes_count: int = 0


class CreateMenuSchema(AbstractMenuShema):
    """Создание меню"""
    pass


class GetSubMenuSchema(AbsractSubMenuSchema):
    """Получение подменю"""
    id: UUID
    dishes_count: int = 0


class CreateSubMenuSchema(AbsractSubMenuSchema):
    """Создание подменю"""
    pass



