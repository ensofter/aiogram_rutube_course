from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User


async def orm_add_user(session: AsyncSession, tg_id: int):
    obj = User(
        tg_id=tg_id,
        is_hold=False
    )
    session.add(obj)
    await session.commit()


async def orm_get_user(session: AsyncSession, tg_id: int):
    query = select(User).where(User.tg_id == tg_id)
    result = await session.execute(query)
    return result.scalar()


async def orm_update_user(session: AsyncSession, tg_id: int, user_data: dict):
    result = await session.execute(
        select(User).where(User.tg_id == tg_id)
    )
    user = result.scalar_one_or_none()
    if user:
        user.name = user_data['name']
        user.age = user_data['age']
        user.gender = user_data['gender']
        user.photo = user_data['photo_id']
        user.education = user_data['education']
        user.wish_news = user_data['wish_news']
        await session.commit()
    else:
        raise ValueError(f'Пользователя с tg_id {tg_id} не существует!')
