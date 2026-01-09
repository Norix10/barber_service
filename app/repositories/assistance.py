from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.assistance import Assistance
from app.schemas.assistance import AssistanceSchema


class AssistanceRepository:
    @staticmethod
    async def get_by_id(assistance_id: int, session: AsyncSession) -> Assistance | None:
        return await session.get(Assistance, assistance_id)

    @staticmethod
    async def get_all(session: AsyncSession) -> list[AssistanceSchema]:
        result = await session.execute(select(Assistance))
        assistances = result.scalars().all()
        return [
            AssistanceSchema.model_validate(assistance, from_attributes=True)
            for assistance in assistances
        ]

    @staticmethod
    async def add(assistance: Assistance, session: AsyncSession) -> Assistance:
        session.add(assistance)
        await session.commit()
        await session.refresh(assistance)
        return assistance

    @staticmethod
    async def update(assistance: Assistance, session: AsyncSession):
        session.add(assistance)
        await session.commit()
        await session.refresh(assistance)
        return assistance

    @staticmethod
    async def delete(assistance: Assistance, session: AsyncSession) -> None:
        await session.delete(assistance)
        await session.commit()
