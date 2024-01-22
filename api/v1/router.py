from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from .models import Menu
from .schemas import MenuDTO

router = APIRouter(
    prefix="/api/v1/menus",
    tags=["Menus"]
)


@router.get("/")
async def root(session: AsyncSession = Depends(get_async_session)):
    query = select(Menu)
    # print(query)
    # result = list(await session.scalars(query))
    result = await session.execute(query)
    result_orm = result.scalars().all()
    # print(result_orm)
    result_dto = [MenuDTO.model_validate(row, from_attributes=True) for row in result_orm]
    # print(result_dto)

    return result_dto


# @router.post('/')
# async def add_restaurant(new_restaurant: RestaurantAdd, sessions: AsyncSession = Depends(get_async_session)):
#     return {'status': 'success', 'message': ''}
