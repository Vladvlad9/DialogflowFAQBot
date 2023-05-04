from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, update, delete, and_

from models import User, create_async_session
from schemas import UsersSchema, UsersInDBSchema


class CRUDUser(object):

    @staticmethod
    @create_async_session
    async def add(user: UsersSchema, session: AsyncSession = None) -> UsersInDBSchema | None:
        users = User(
            **user.dict()
        )
        session.add(users)
        try:
            await session.commit()
        except IntegrityError as e:
            print(e)
        else:
            await session.refresh(users)
            return UsersInDBSchema(**users.__dict__)

    @staticmethod
    @create_async_session
    async def get(user_id: int, session: AsyncSession = None) -> UsersInDBSchema | None:
        user = await session.execute(
            select(User).where(User.user_id == user_id)
        )
        if users := user.first():
            return UsersInDBSchema(**users[0].__dict__)

    @staticmethod
    @create_async_session
    async def update(user: UsersInDBSchema, session: AsyncSession = None) -> None:
        await session.execute(
            update(User)
            .where(User.id == user.id)
            .values(**user.dict())
        )
        await session.commit()
