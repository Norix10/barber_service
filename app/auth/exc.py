from http import HTTPStatus

from fastapi import status

from app.services.exc.base import IException


class UnauthorizedException(IException):
    _status_code: HTTPStatus = status.HTTP_403_FORBIDDEN


class UnauthenticatedException(IException):
    _status_code: HTTPStatus = status.HTTP_401_UNAUTHORIZED

    def __init__(self):
        super().__init__("Requires authentication")


class NotFoundException(IException):
    _status_code: HTTPStatus = status.HTTP_404_NOT_FOUND

    def __init__(self):
        super().__init__("User not found")
