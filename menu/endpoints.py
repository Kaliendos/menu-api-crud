from typing import List

from fastapi import APIRouter, Depends, Request, Body

from . import schemas
from .operations import MenuOperations, SubMenuOperations, DishOperation


router = APIRouter(
    prefix="/api/v1"
)

# Меню роутеры
@router.get("/menus", response_model=List[schemas.GetMenuSchema])
def get_menu_list(operation: MenuOperations = Depends()):
    return operation.get_menu_list()


@router.get("/menus/{menu_id}", response_model=schemas.GetMenuSchema)
def get_menu_by_id(menu_id, operation: MenuOperations = Depends()):
    return operation.get_menu_by_id(menu_id)


@router.post("/menus", response_model=schemas.GetMenuSchema, status_code=201)
def create_menu(request_data: schemas.PostMenuSchema, operation: MenuOperations = Depends()):
    return operation.create_menu(request_data)


@router.patch("/menus/{menu_id}", response_model=schemas.GetMenuSchema)
def patch_menu(
        menu_id,
        request_data: schemas.PatchMenuSchema,
        operation: MenuOperations = Depends()):
    return operation.patch_menu(menu_id, request_data)


@router.delete("/menus/{menu_id}")
def delete_menu(
        menu_id,
        operation: MenuOperations = Depends()):
    return operation.delete_menu(menu_id)


# Подменю роутеры
@router.post("/menus/{menu_id}/submenus",
             response_model=schemas.GetSubMenuSchema,
             status_code=201)
def create_sub_menu(
        menu_id,
        request_data: schemas.CreateSubMenuSchema,
        operation: SubMenuOperations = Depends(),
):
    return operation.create_submenu(menu_id, request_data)


@router.get("/menus/{menu_id}/submenus", response_model=List[schemas.GetSubMenuSchema])
def get_submenus_list(
        menu_id,
        operation: SubMenuOperations = Depends(),
):
    return operation.get_sub_menu_list(menu_id)


@router.get("/menus/{menu_id}/submenus/{submenu_id}", response_model=schemas.GetSubMenuSchema)
def get_submenu_by_id(
        submenu_id,
        operation: SubMenuOperations = Depends(),
):
    return operation.get_submenu_by_id(submenu_id)

@router.patch("/menus/{menu_id}/submenus/{submenu_id}", response_model=schemas.GetSubMenuSchema)
def patch_submenu(
        submenu_id,
        request_data: schemas.PatchMenuSchema,
        operation: SubMenuOperations = Depends(),
):
    return operation.patch_submenu(submenu_id, request_data)

@router.delete("/menus/{menu_id}/submenus/{submenu_id}")
def delete_submenu(
        submenu_id,
        operation: SubMenuOperations = Depends(),
):
     operation.delete_submenu(submenu_id)
     return {"status": True, "message": "The submenu has been deleted"}

# Блюда роутеры
@router.post("/menus/{menu_id}/submenus/{submenu_id}/dishes",
             response_model=schemas.DishSchema)
def create_dish(
        submenu_id,
        request_data: schemas.DishSchema,
        operation: DishOperation = Depends(),
):
    return operation.create_dish(submenu_id, request_data)


@router.get("/menus/{menu_id}/submenus/{submenu_id}/dishes",
             response_model=List[schemas.DishSchema])
def create_dish_list(
        submenu_id,
        operation: DishOperation = Depends(),
):
    return operation.get_dish_list(submenu_id)


@router.get("/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
            response_model=schemas.DishSchema)
def create_dish_item(
        submenu_id,
        dish_id,
        operation: DishOperation = Depends(),
):
    return operation.get_dish_item(submenu_id, dish_id)


