from fastapi import HTTPException, status
from http import HTTPStatus

class IException(Exception):
    _status_code: HTTPStatus = HTTPStatus.NOT_FOUND
    _message: str = ""

    def __init__(self, message: str):
        self._message = message
        super().__init__(message)

    @property
    def status_code(self):
        return self._status_code

    @property
    def message(self):
        return self._message
    
class IEntytyException(IException):
    _entity_name: str

class EntytyIDIsBusyException(IEntytyException):
    _status_code: HTTPStatus = HTTPStatus.CONFLICT

    def __init__(self, entity_id: id):
        super().__init__(f"{self._entity_name} with id {entity_id} exists.")


class UnauthenticatedException(HTTPException):
    def __init__(self, detail: str = "Could not validate credentials"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class UnauthorizedException(HTTPException):
    def __init__(self, detail: str = "Not enough permissions"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )


class NotFoundException(HTTPException):
    def __init__(self, detail:str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
