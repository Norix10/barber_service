from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.barbers import Barbers
from app.schemas.barbers import BarberSchema

class BarbersRepository:
    @staticmethod
    async def get_by_id(barber_id: int, session: AsyncSession) -> Barbers | None:
        return await session.get(Barbers, barber_id)

    @staticmethod
    async def get_by_email(email: str, session: AsyncSession) -> Barbers | None:
        result = await session.execute(select(Barbers).where(Barbers.email == email))
        barber = result.scalars().first()
        return barber

    @staticmethod
    async def get_all(session: AsyncSession) -> list[BarberSchema]:
        result = await session.execute(select(Barbers))
        barbers = result.scalars().all()
        return [BarberSchema.model_validate(
            barber, from_attributes=True
        ) for barber in barbers]

    @staticmethod
    async def add(barber: Barbers, session: AsyncSession) -> Barbers:
        session.add(barber)
        await session.commit()
        await session.refresh(barber)
        return barber

    @staticmethod
    async def update(barber: Barbers, session: AsyncSession) -> Barbers:
        session.add(barber)
        await session.commit()
        await session.refresh(barber)
        return barber

    @staticmethod
    async def delete(barber: Barbers, session: AsyncSession) -> None:
        await session.delete(barber)
        await session.commit()