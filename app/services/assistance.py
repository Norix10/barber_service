from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.repositories.assistance import AssistanceRepository
from app.models.assistance import Assistance
from app.schemas.assistance import (
    AssistanceSchema,
    AssistanceCreateSchema,
    AssistanceUpdateSchema,
)
from app.services.exc.base import NotFoundException


class AssistanceService:
    def __init__(self) -> None:
        self._repository = AssistanceRepository()

    async def get_assistance_or_erorr(self, assistance_id: int, session: AsyncSession):
        assistance = await self._repository.get_by_id(assistance_id, session)
        if not assistance:
            raise NotFoundException("Assistance is not found")
        return assistance

    async def get_list(self, session: AsyncSession) -> list[Assistance]:
        return await self._repository.get_all(session)

    async def create(self, data: AssistanceCreateSchema, session: AsyncSession) -> Assistance:
        assistance = Assistance(
            name=data.name,
            price=data.price,
            duration_minutes=data.duration_minutes,
            description=data.description,
        )
        return await self._repository.add(assistance, session)

    async def update(
        self,
        assistance_id: int,
        data: AssistanceUpdateSchema,
        session: AsyncSession,
    ) -> Assistance:
        assistance = await self.get_assistance_or_erorr(assistance_id, session)
        if data.name is not None:
            assistance.name = data.name
        if data.price is not None:
            assistance.price = data.price
        if data.duration_minutes is not None:
            assistance.duration_minutes = data.duration_minutes
        if data.description is not None:
            assistance.description = data.description
        return await self._repository.update(assistance, session)

    async def delete(self, assistance: Assistance, session: AsyncSession) -> None:
        await self._repository.delete(assistance, session)


async def get_assistance_service() -> AssistanceService:
    return AssistanceService()
