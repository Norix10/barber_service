from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.repositories.admin import AdminRepository
from app.models.admin import Admin
from app.schemas.admin import (
    AdminSignInSchema,
)
from app.schemas.jwt import TokenSchema, TokenDataSchema
from app.utils.security import verify_password, get_password_hash
from app.auth.token import create_access_token
from app.services.exc.base import NotFoundException


class AdminService:
    def __init__(self) -> None:
        self._repository = AdminRepository()

    async def get_by_email(self, email: str, session: AsyncSession) -> Admin:
        admin = await self._repository.get_by_email(email, session)
        if not admin:
            raise NotFoundException
        return admin

    async def authenticate(
        self, data: AdminSignInSchema, session: AsyncSession
    ) -> TokenSchema:
        admin = await self._repository.get_by_email(data.email, session)
        if not admin or not verify_password(data.password, admin.hashed_password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        token_data = TokenDataSchema(sub=admin.email)
        access_token = create_access_token(data=token_data)
        return TokenSchema(access_token=access_token, token_type="bearer")


async def get_admin_service() -> AdminService:
    return AdminService()
