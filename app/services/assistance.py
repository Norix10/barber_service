from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.repositories.assistance import AssistanceRepository
from app.models.services import Service
from app.schemas.assistance import (
    ServiceSchema,
    ServiceCreateSchema,
    ServiceUpdateSchema,
)
from app.services.exc.base import NotFoundException


class AssistanceService:
    def __init__(self) -> None:
        self._repository = AssistanceRepository()

    async def get_assistance_or_erorr(self, service_id: int, session: AsyncSession):
        assistance = await self._repository.get_by_id(service_id, session)
        if not assistance:
            raise NotFoundException("Assistance is not found")
        return assistance

    async def get_list(self, session: AsyncSession) -> list[ServiceSchema]:
        return await self._repository.get_all(session)

    async def create(self, data: ServiceCreateSchema, session: AsyncSession) -> Service:
        assistance = Service(
            name=data.name,
            price=data.price,
            duration_minutes=data.duration_minutes,
            description=data.description,
        )
        return await self._repository.add(assistance, session)

    async def update(
        self,
        service_id: int,
        data: ServiceUpdateSchema,
        session: AsyncSession,
    ) -> Service:
        assistance = await self.get_assistance_or_erorr(service_id, session)
        if data.name:
            assistance.name = data.name
        if data.price:
            assistance.price = data.price
        if data.duration_minutes:
            assistance.duration_minutes = data.duration_minutes
        if data.description:
            assistance.description = data.description
        return await self._repository.update(assistance, session)

    async def delete(self, assistance: Service, session: AsyncSession) -> None:
        await self._repository.delete(assistance, session)


async def get_assistance_service() -> AssistanceService:
    return AssistanceService()
