"""Users Service Interface. Controller는 이 인터페이스에만 의존한다."""

from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from domains.users.schemas import UserResponse


class UserServiceInterface(ABC):
    @abstractmethod
    def get_by_id(self, db: Session, user_id: int) -> UserResponse | None:
        """사용자 ID로 조회."""
        ...
