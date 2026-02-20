"""Users Controller. Service에 위임하며 DB 세션을 주입받는다."""

from sqlalchemy.orm import Session

from domains.users.schemas import UserResponse
from domains.users.service.user_service import UserServiceInterface


class UserController:
    def __init__(self, service: UserServiceInterface, db: Session) -> None:
        self._service = service
        self._db = db

    def get_by_id(self, user_id: int) -> UserResponse | None:
        """사용자 ID로 조회."""
        return self._service.get_by_id(self._db, user_id)
