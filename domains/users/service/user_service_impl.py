"""Users Service 구현체. DB 세션을 받아 조회/변경한다."""

from sqlalchemy.orm import Session

from domains.users.schemas import UserResponse
from domains.users.service.user_service import UserServiceInterface
from models import User


class UserServiceImpl(UserServiceInterface):
    def get_by_id(self, db: Session, user_id: int) -> UserResponse | None:
        user = db.get(User, user_id)
        if not user:
            return None
        return UserResponse(
            id=user.id,
            kakao_id=user.kakao_id,
            email=user.email,
            nickname=user.nickname,
            profile_image_url=user.profile_image_url,
        )
