"""Users Controller. Service에 위임하며 DB 세션을 주입받는다."""

from sqlalchemy.orm import Session

from domains.users.schemas import UserRead, UserResponse, UserUpdate
from domains.users.service.user_service import UserServiceInterface


class UserController:
    def __init__(self, service: UserServiceInterface, db: Session) -> None:
        self._service = service
        self._db = db

    def get_by_id(self, user_id: int) -> UserResponse | None:
        """사용자 ID로 조회."""
        return self._service.get_by_id(self._db, user_id)

    def get_me(self, user_id: int) -> UserRead | None:
        """로그인 사용자 본인 정보 조회 (마이페이지)."""
        return self._service.get_me(self._db, user_id)

    def update_settings(self, user_id: int, data: UserUpdate) -> UserRead | None:
        """알림 설정 및 닉네임 수정."""
        return self._service.update_settings(self._db, user_id, data)
