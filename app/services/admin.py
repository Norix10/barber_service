from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.admin import AdminRepository
from app.models.admin import Admin
from app.schemas.admin import AdminCreate


class AdminService:
    def __init__(self) -> None:
        self._repository = AdminRepository()

    async def create(self, data: AdminCreate, session: AsyncSession) -> Admin:
        admin = Admin(
            name=data.name,
            email=data.email,
            hashed_password=data.password
        )
        return await self._repository.add(admin, session)


async def get_admin_service() -> AdminService:
    return AdminService()