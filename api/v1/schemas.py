from decimal import Decimal

from pydantic import BaseModel, UUID4


class MenuAddDTO(BaseModel):
    title: str
    description: str


class MenuDTO(MenuAddDTO):
    id: UUID4
    submenus_count: int
    dishes_count: int


class MenuUpdateDTO(BaseModel):
    title: str | None
    description: str | None


class MenuDeleteDTO(BaseModel):
    status: bool = True
    message: str = "The menu has been deleted"


class SubMenuAddDTO(BaseModel):
    title: str
    description: str


class SubMenuDTO(SubMenuAddDTO):
    id: UUID4
    dishes_count: int


class SubMenuUpdateDTO(BaseModel):
    title: str | None
    description: str | None


class SubMenuDeleteDTO(BaseModel):
    status: bool = True
    message: str = "The submenu has been deleted"


class DishAddDTO(BaseModel):
    title: str
    description: str
    price: Decimal


class DishDTO(DishAddDTO):
    id: UUID4
