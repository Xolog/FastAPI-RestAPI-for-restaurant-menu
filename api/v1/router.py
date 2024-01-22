from typing import List

from sqlalchemy import select, insert
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from .models import Menu, Submenu, Dish
from database import get_async_session
from .schemas import MenuDTO, MenuAddDTO, MenuUpdateDTO, MenuDeleteDTO, SubMenuDTO, SubMenuAddDTO, SubMenuUpdateDTO, \
    SubMenuDeleteDTO, DishDTO, DishAddDTO, DishUpdateDTO, DishDeleteDTO

menu_router = APIRouter(
    prefix="/api/v1/menus",
    tags=["Menus"]
)



@menu_router.get("/", response_model=List[MenuDTO])
async def get_menu_list(session: AsyncSession = Depends(get_async_session)):
    query = (
        select(Menu)
    )
    # print(query)
    # result = list(await session.scalars(query))
    result = (await session.execute(query)).unique()
    result_orm = result.scalars().all()
    # print(result_orm)
    # result_dto = [MenuDTO.model_validate(row, from_attributes=True) for row in result_orm]
    # print(result_dto)

    return result_orm


@menu_router.post('/', response_model=MenuDTO, status_code=201)
async def add_menu(new_menu: MenuAddDTO, session: AsyncSession = Depends(get_async_session)):
    stmt = Menu(**new_menu.model_dump())
    session.add(stmt)
    await session.commit()

    query = select(Menu).order_by(Menu.id.desc()).limit(1)
    result = await session.execute(query)
    latest_menu_entry = result.scalar()
    # latest_menu_entry_dto = MenuDTO.model_validate(latest_menu_entry[0], from_attributes=True)

    return latest_menu_entry


@menu_router.get('/{api_test_menu_id}', response_model=MenuDTO)
async def get_menu(api_test_menu_id: str, session: AsyncSession = Depends(get_async_session)):
    # query = select(Menu).where(Menu.id == api_test_menu_id)
    # result = await session.execute(query)
    # menu_item = result.scalar()
    menu_item = await session.get(Menu, api_test_menu_id)

    if menu_item is None:
        raise HTTPException(status_code=404, detail="menu not found")

    return menu_item


@menu_router.patch('/{api_test_menu_id}', response_model=MenuDTO)
async def update_menu(api_test_menu_id: str, body: MenuUpdateDTO, session: AsyncSession = Depends(get_async_session)):
    result = await session.get(Menu, api_test_menu_id)

    if result is None:
        raise HTTPException(status_code=404, detail="menu not found")

    for field, value in body.model_dump(exclude_none=True).items():
        setattr(result, field, value)

    await session.commit()

    return result


@menu_router.delete('/{api_test_menu_id}', response_model=MenuDeleteDTO)
async def delete_menu(api_test_menu_id: str, session: AsyncSession = Depends(get_async_session)):
    result = await session.get(Menu, api_test_menu_id)

    await session.delete(result)
    await session.commit()

    return MenuDeleteDTO()


@menu_router.get('/{api_test_menu_id}/submenus', response_model=List[SubMenuDTO])
async def get_submenu_list(api_test_menu_id: str, session: AsyncSession = Depends(get_async_session)):
    menu = await session.get(Menu, api_test_menu_id)
    submenus = menu.submenu
    return submenus


@menu_router.post('/{api_test_menu_id}/submenus', response_model=SubMenuDTO, status_code=201)
async def add_submenu(api_test_menu_id: str, new_sub_menu: SubMenuAddDTO, session: AsyncSession = Depends(get_async_session)):
    stmt = Submenu(**new_sub_menu.model_dump(), menu_id=api_test_menu_id)
    session.add(stmt)
    await session.commit()
    await session.refresh(stmt)

    return stmt


@menu_router.get('/{api_test_menu_id}/submenus/{api_test_submenu_id}', response_model=SubMenuDTO)
async def get_submenu(api_test_menu_id: str, api_test_submenu_id: str, session: AsyncSession = Depends(get_async_session)):
    query = select(Submenu).filter(Submenu.id == api_test_submenu_id, Submenu.menu_id == api_test_menu_id)

    result = await session.scalar(query)
    if result is None:
        raise HTTPException(status_code=404, detail="submenu not found")

    return result


@menu_router.patch('/{api_test_menu_id}/submenus/{api_test_submenu_id}', response_model=SubMenuDTO)
async def patch_submenu(api_test_menu_id: str, api_test_submenu_id: str, body: SubMenuUpdateDTO, session: AsyncSession = Depends(get_async_session)):
    query = select(Submenu).filter(Submenu.id == api_test_submenu_id, Submenu.menu_id == api_test_menu_id)

    result = await session.scalar(query)
    if result is None:
        raise HTTPException(status_code=404, detail="submenu not found")

    for field, value in body.model_dump(exclude_none=True).items():
        setattr(result, field, value)

    await session.commit()

    return result


@menu_router.delete('/{api_test_menu_id}/submenus/{api_test_submenu_id}', response_model=SubMenuDeleteDTO)
async def delete_submenu(api_test_menu_id: str, api_test_submenu_id: str, session: AsyncSession = Depends(get_async_session)):
    query = select(Submenu).filter(Submenu.id == api_test_submenu_id, Submenu.menu_id == api_test_menu_id)

    result = await session.scalar(query)

    await session.delete(result)
    await session.commit()

    return SubMenuDeleteDTO()


@menu_router.get('/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes', response_model=List[DishDTO])
async def get_dish_list(api_test_menu_id: str, api_test_submenu_id: str, session: AsyncSession = Depends(get_async_session)):
    query = select(Submenu).filter(Submenu.id == api_test_submenu_id, Submenu.menu_id == api_test_menu_id)
    result = await session.scalar(query)

    return result.dish


@menu_router.post('/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes', response_model=DishDTO, status_code=201)
async def add_dish_list(api_test_menu_id: str, api_test_submenu_id: str, new_dish: DishAddDTO, session: AsyncSession = Depends(get_async_session)):
    stmt = Dish(**new_dish.model_dump(), submenu_id=api_test_submenu_id)
    session.add(stmt)
    await session.commit()
    await session.refresh(stmt)

    return stmt


@menu_router.get('/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{dish_id}', response_model=DishDTO)
async def get_submenu(api_test_menu_id: str, api_test_submenu_id: str, dish_id: str, session: AsyncSession = Depends(get_async_session)):
    query = select(Dish).filter(Dish.id == dish_id)

    result = await session.scalar(query)
    if result is None:
        raise HTTPException(status_code=404, detail="dish not found")

    return result


@menu_router.patch('/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{dish_id}', response_model=DishUpdateDTO)
async def patch_submenu(api_test_menu_id: str, api_test_submenu_id: str,  dish_id: str, body: DishUpdateDTO, session: AsyncSession = Depends(get_async_session)):
    query = select(Dish).filter(Dish.id == dish_id)

    result = await session.scalar(query)
    if result is None:
        raise HTTPException(status_code=404, detail="dish not found")

    for field, value in body.model_dump(exclude_none=True).items():
        setattr(result, field, value)

    await session.commit()

    return result


@menu_router.delete('/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{dish_id}', response_model=DishDeleteDTO)
async def delete_menu(api_test_menu_id: str, api_test_submenu_id: str, dish_id: str, session: AsyncSession = Depends(get_async_session)):
    query = select(Dish).filter(Dish.id == dish_id)

    result = await session.scalar(query)

    await session.delete(result)
    await session.commit()

    return DishDeleteDTO()
