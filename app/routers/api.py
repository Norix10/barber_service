from fastapi import APIRouter

from app.routers.v1 import (
    admin,
    user,
    barbers,
    assistance,
    appointments,
)

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(admin.router)
api_router.include_router(user.router)
api_router.include_router(barbers.router)
api_router.include_router(assistance.router)
api_router.include_router(appointments.router)