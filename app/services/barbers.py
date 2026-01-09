from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.utils.security import get_password_hash, verify_password
from app.schemas.jwt import TokenDataSchema, TokenSchema
from app.auth.token import create_access_token
from app.services.exc.base import NotFoundException, ConflictException
from app.services.exc.user import UserEmailIsBusyException

from app.repositories.barbers import BarbersRepository
from app.schemas.barbers import (
    BarberSchema,
    BarberCreateSchema,
    BarberUpdateSchema,
)
from app.models.barbers import Barbers


class BarbersService:
    def __init__(self) -> None:
        self._repository = BarbersRepository()

    async def get_by_email(self, email: str, session: AsyncSession):
        barber = await self._repository.get_by_email(email, session)
        if not barber:
            raise NotFoundException
        return barber

    async def get_barber_or_error(self, barber_id: int, session: AsyncSession):
        barber = await self._repository.get_by_id(barber_id, session)
        if not barber:
            raise NotFoundException("Barber is not found")
        return barber

    async def validate_email(self, email: str, session: AsyncSession):
        if await self._repository.get_by_email(email, session):
            raise UserEmailIsBusyException(email)

    async def create(self, data: BarberCreateSchema, session: AsyncSession) -> Barbers:
        if data.id and await self._repository.get_by_id(data.id, session):
            raise ConflictException

        await self.validate_email(data.email, session)

        barber = Barbers(
            name=data.name,
            email=data.email,
            hashed_password=get_password_hash(data.password),
            phone_number=data.phone_number,
            division=data.division,
            is_free=data.is_free,
            rating=data.rating,
        )
        return await self._repository.add(barber, session)

    async def get_list(self, session: AsyncSession) -> list[BarberSchema]:
        return await self._repository.get_all(session)

    async def update(
        self,
        barber_id: int,
        data: BarberUpdateSchema,
        session: AsyncSession,
    ) -> Barbers:
        barber = await self.get_barber_or_error(barber_id, session)
        if data.name is not None:
            barber.name = data.name
        if data.email is not None:
            barber.email = data.email
        if data.phone_number is not None:
            barber.phone_number = data.phone_number
        if data.division is not None:
            barber.division = data.division
        if data.is_free is not None:
            barber.is_free = data.is_free
        if data.rating is not None:
            barber.rating = data.rating
        if data.password is not None:
            barber.hashed_password = get_password_hash(data.password)
        return await self._repository.update(barber, session)

    async def delete(self, barber: Barbers, session: AsyncSession) -> None:
        await self._repository.delete(barber, session)


async def get_barbers_service() -> BarbersService:
    return BarbersService()
