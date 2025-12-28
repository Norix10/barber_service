from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.utils.security import get_password_hash, verify_password
from app.repositories.user import UserRepository
from app.schemas.jwt import TokenSchema, TokenDataSchema
from app.schemas.user import (
    UserSchema,
    UserCreateSchema,
    UserSignInSchema,
    UserUpdateSchema,
)
from app.models.user import User
from app.auth.token import create_access_token
from app.services.exc.base import NotFoundException, ConflictException
from app.services.exc.user import UserEmailIsBusyException


class UserService:
    def __init__(self) -> None:
        self._repository = UserRepository()

    async def get_by_email(self, email: str, session: AsyncSession) -> User:
        user = await self._repository.get_by_email(email, session)
        if not user:
            raise NotFoundException
        return user

    async def get_user_or_error(self, user_id: int, session: AsyncSession):
        user = await self._repository.get_by_id(user_id, session)
        if not user:
            raise NotFoundException
        return user

    async def validate_email(self, email: str, session: AsyncSession):
        if await self._repository.get_by_email(email, session):
            raise UserEmailIsBusyException(email)

    async def get_list(self, session: AsyncSession) -> list[UserSchema]:
        return await self._repository.get_all(session)

    async def authenticate(
        self, data: UserSignInSchema, session: AsyncSession
    ) -> TokenSchema:
        user = await self._repository.get_by_email(data.email, session)
        if not user or not verify_password(data.password, user.hashed_password):
            raise NotFoundException

        token_data = TokenDataSchema(sub=user.email)
        access_token = create_access_token(data=token_data)
        return TokenSchema(access_token=access_token, token_type="bearer")

    async def create(self, data: UserCreateSchema, session: AsyncSession) -> User:
        if data.id and await self._repository.get_by_id(data.id, session):
            raise ConflictException

        await self.validate_email(data.email, session)

        user = User(
            name=data.name,
            email=data.email,
            hashed_password=get_password_hash(data.password),
        )
        return await self._repository.add(user, session)

    async def update(
        self, current_user_id: int, data: UserUpdateSchema, session: AsyncSession
    ) -> User:
        user = await self.get_user_or_error(current_user_id, session)
        if data.name:
            user.name = data.name
        if data.password:
            user.hashed_password = get_password_hash(data.password)
        return await self._repository.update(user, session)

    async def delete(self, user: User, session: AsyncSession):
        await self._repository.delete(user, session)


async def get_user_service() -> UserService:
    return UserService()
