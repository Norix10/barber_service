from http import HTTPStatus

from app.models.user import User
from http import HTTPStatus

from app.models.user import User
from app.services.exc.base import IEntytyException

class UserEmailIsBusyException(IEntytyException):
    _entity_name: str = User.__name__
    _status_code: HTTPStatus = HTTPStatus.CONFLICT

    def __init__(self, email: str):
        super().__init__(f"{self._entity_name} with email {email} exists.")