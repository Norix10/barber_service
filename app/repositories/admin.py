from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.admin import Admin
# from app.schemas.admin import AdminSchema

class AdminRepository:
    @staticmethod
    async def add(admin: Admin, session: AsyncSession) -> Admin:
        session.add(admin)
        await session.commit()
        await session.refresh(admin)
        return admin