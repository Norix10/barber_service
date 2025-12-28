from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.admin import Admin
from app.schemas.admin import AdminSchema

class AdminRepository:
    @staticmethod
    async def get_by_id(admin_id: int, session:AsyncSession) -> Admin | None:
        return await session.get(Admin, admin_id)
    
    @staticmethod
    async def get_by_email(email:str, session:AsyncSession) -> Admin | None:
        result = await session.execute(select(Admin).where(Admin.email == email))
        user = result.scalars().first()
        return user
    
    