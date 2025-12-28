from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.services import Service
from app.schemas.assistance import ServiceBaseSchema


class AssistanceRepository:
    @staticmethod
    async def get_by_id(assistance_id: int, session: AsyncSession) -> Service | None:
        return await session.get(Service, assistance_id)

    @staticmethod
    async def get_all(session: AsyncSession) -> list[ServiceBaseSchema]:
        result = await session.execute(select(Service))
        assistances = result.scalars().all()
        return [
            ServiceBaseSchema.model_validate(assistance, from_attributes=True)
            for assistance in assistances
        ]

    @staticmethod
    async def add(assistance: Service, session: AsyncSession) -> Service:
        session.add(assistance)
        await session.commit()
        await session.refresh(assistance)
        return assistance

    @staticmethod
    async def update(assistance: Service, session: AsyncSession):
        session.add(assistance)
        await session.commit()
        await session.refresh(assistance)
        return assistance

    @staticmethod
    async def delete(assistance: Service, session: AsyncSession) -> None:
        await session.delete(assistance)
        await session.commit()
