from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.schemas.user import UserSchema

class UserRepository:
    @staticmethod
    async def get_by_id(user_id: int, session: AsyncSession) -> User | None:
        return await session.get(User, user_id)

    @staticmethod
    async def get_by_email(email: str, session: AsyncSession) -> User | None:
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        return user

    @staticmethod
    async def get_all(session: AsyncSession) -> list[UserSchema]:
        result = await session.execute(select(User))
        users = result.scalars().all()
        return [UserSchema.model_validate(
            user, from_attributes=True
        ) for user in users]

    @staticmethod
    async def add(user: User, session: AsyncSession) -> User:
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def update(user: User, session: AsyncSession) -> User:
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def delete(user: User, session: AsyncSession) -> None:
        await session.delete(user)
        await session.commit()
