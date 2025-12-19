from fastapi import APIRouter, Depends

from app.core.config import settings
from app.db.database import AsyncSession, get_db_session
from app.services.admin import AdminService, get_admin_service
from app.schemas.admin import AdminCreate, AdminResponse
from app.models.admin import Admin

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/create-new-user", response_model=AdminResponse)
async def create_new_user(
    data: AdminCreate,
    admin_service: AdminService = Depends(get_admin_service),
    session: AsyncSession = Depends(get_db_session),
) -> Admin:
    return await admin_service.create(data, session)
