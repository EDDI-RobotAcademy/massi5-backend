"""Users Service Interface. Controller는 이 인터페이스에만 의존한다."""

from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from domains.users.schemas import UserRead, UserResponse, UserUpdate


class UserServiceInterface(ABC):
    @abstractmethod
    def get_by_id(self, db: Session, user_id: int) -> UserResponse | None:
        """사용자 ID로 조회."""
        ...

    @abstractmethod
    def get_me(self, db: Session, user_id: int) -> UserRead | None:
        """로그인 사용자 본인 정보 조회 (마이페이지)."""
        ...

    @abstractmethod
    def update_settings(self, db: Session, user_id: int, data: UserUpdate) -> UserRead | None:
        """알림 설정 및 닉네임 수정 (PATCH /users/me/settings)."""
        ...
