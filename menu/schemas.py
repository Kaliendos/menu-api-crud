from uuid import UUID

from pydantic import BaseModel


class BaseMenuShema(BaseModel):
    """Абстрактный класс для операций меню"""
    title: str
    description: str

    class Config:
        orm_mode = True


class PostMenuSchema(BaseMenuShema):
    pass


class GetMenuSchema(BaseMenuShema):
    id: UUID
    submenus_count: int = 0
    dishes_count: int = 0


class PatchMenuSchema(BaseModel):
    title: str | None
    description: str| None


class PatchSubMenuSchema(BaseModel):
    title: str | None
    description: str| None


class AbsractSubMenuSchema(BaseModel):
    """Абстрактный класс для операций SubMenu"""
    title: str
    description: str

    class Config:
        orm_mode = True


class GetSubMenuSchema(AbsractSubMenuSchema):
    """Получение подменю"""
    id: UUID
    dishes_count: int = 0


class CreateSubMenuSchema(AbsractSubMenuSchema):
    """Создание подменю"""
    pass


class DeleteSubmenuSchema(BaseModel):
    status: bool = True
    message: str = "The submenu has been deleted"


class DishSchema(BaseModel):
    id: UUID | None
    title: str
    description: str
    price: str

    class Config:
        orm_mode = True



