from uuid import UUID

from pydantic import BaseModel


class BaseMenuShema(BaseModel):
    """Базовая схема для меню"""
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
    description: str | None


class PatchSubMenuSchema(BaseModel):
    title: str | None
    description: str | None


class BaseSubMenuSchema(BaseModel):
    """Базовый класс для SubMenu"""
    title: str
    description: str

    class Config:
        orm_mode = True


class GetSubMenuSchema(BaseSubMenuSchema):
    """Получение подменю"""
    id: UUID
    dishes_count: int = 0


class CreateSubMenuSchema(BaseSubMenuSchema):
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


class UpdateDishSchema(BaseModel):
    id: UUID | None
    title: str | None
    description: str | None
    price: str | None

    class Config:
        orm_mode = True
