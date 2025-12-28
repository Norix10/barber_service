import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, SecurityScopes, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.exc import UnauthenticatedException, NotFoundException
from app.core.config import settings
from app.db.database import get_db_session
from app.models.user import User
from app.services.user import get_user_service, UserService
from app.services.admin import get_admin_service, AdminService

class JWTAuth:
    def decode_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
            return payload
        except jwt.ExpiredSignatureError:
            raise UnauthenticatedException("Token has expired")
        except jwt.InvalidTokenError:
            raise UnauthenticatedException("Invalid token")

    def get_entity_email_from_payload(self, payload: dict) -> str:
        email: str | None = payload.get("sub")
        if email is None:
            raise UnauthenticatedException("Token payload invalid: missing 'sub' field")
        return email

    async def get_current_user(
        self,
        token: HTTPAuthorizationCredentials,
        session: AsyncSession,
        user_service: UserService,
    ) -> User:
        payload = self.decode_token(token.credentials)
        email = self.get_entity_email_from_payload(payload)

        try:
            user = await user_service.get_by_email(email, session)
        except NotFoundException:
            raise UnauthenticatedException("User not found")

        return user

    async def get_current_admin(
        self,
        token: HTTPAuthorizationCredentials,
        session: AsyncSession,
        admin_service: AdminService,
    ) -> User:
        payload = self.decode_token(token.credentials)
        email = self.get_entity_email_from_payload(payload)

        try:
            admin = await admin_service.get_by_email(email, session)
        except NotFoundException:
            raise UnauthenticatedException("Admin not found")

        return admin


jwt_auth = JWTAuth()


async def get_current_user(
    security_scopes: SecurityScopes,
    token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    session: AsyncSession = Depends(get_db_session),
    user_service: UserService = Depends(get_user_service)
) -> User:
    return await jwt_auth.get_current_user(token, session, user_service)

async def get_current_admin(
    security_scopes: SecurityScopes,
    token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    session: AsyncSession = Depends(get_db_session),
    admin_service: UserService = Depends(get_admin_service)
) -> User:
    return await jwt_auth.get_current_admin(token, session, admin_service)