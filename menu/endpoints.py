from typing import List

from fastapi import APIRouter, Depends

from . import schemas
from .operations import MenuOperations, SubMenuOperations
from .schemas import GetMenuSchema, CreateMenuSchema

router = APIRouter(
    prefix="/api/v1"
)


@router.get("/menus", response_model=List[GetMenuSchema])
def get_menu_list(operation: MenuOperations = Depends()):
    return operation.get_menu_list()


@router.get("/menus/{menu_id}", response_model=GetMenuSchema)
def get_menu_by_id(menu_id, operation: MenuOperations = Depends()):
    return operation.get_menu_by_id(menu_id)


@router.post("/menus", response_model=CreateMenuSchema, status_code=201)
def create_menu(request_data: CreateMenuSchema, operation: MenuOperations = Depends()):
    return operation.create_menu(request_data)


@router.post(r'/menus/{menu_id}/submenus')
def create_sub_menu(
        menu_id,
        request_data: schemas.CreateSubMenuSchema,
        operation: SubMenuOperations = Depends(),
):
    return operation.create_submenu(menu_id, request_data)