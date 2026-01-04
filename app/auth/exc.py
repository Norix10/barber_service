from http import HTTPStatus
from fastapi import HTTPException, status

from app.services.exc.base import IException


class UnauthorizedException(IException):
    _status_code: HTTPStatus = status.HTTP_403_FORBIDDEN

class UnauthenticatedException(HTTPException):
    def __init__(self, detail: str = "Token has been expired"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
        )


class NotFoundException(IException):
    _status_code: HTTPStatus = status.HTTP_404_NOT_FOUND

    def __init__(self):
        super().__init__("User not found")
