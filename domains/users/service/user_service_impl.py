"""Users Service 구현체. DB 세션을 받아 조회/변경한다."""

from sqlalchemy.orm import Session

from domains.users.schemas import UserRead, UserResponse, UserUpdate
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

    def get_me(self, db: Session, user_id: int) -> UserRead | None:
        user = db.get(User, user_id)
        if not user:
            return None
        return UserRead(
            id=user.id,
            kakao_id=user.kakao_id,
            email=user.email,
            nickname=user.nickname,
            profile_image_url=user.profile_image_url,
            is_lunch_alarm_on=user.is_lunch_alarm_on,
            is_report_alarm_on=user.is_report_alarm_on,
        )

    def update_settings(self, db: Session, user_id: int, data: UserUpdate) -> UserRead | None:
        user = db.get(User, user_id)
        if not user:
            return None
        if data.nickname is not None:
            user.nickname = data.nickname
        if data.is_lunch_alarm_on is not None:
            user.is_lunch_alarm_on = data.is_lunch_alarm_on
        if data.is_report_alarm_on is not None:
            user.is_report_alarm_on = data.is_report_alarm_on
        db.add(user)
        db.commit()
        db.refresh(user)
        return UserRead(
            id=user.id,
            kakao_id=user.kakao_id,
            email=user.email,
            nickname=user.nickname,
            profile_image_url=user.profile_image_url,
            is_lunch_alarm_on=user.is_lunch_alarm_on,
            is_report_alarm_on=user.is_report_alarm_on,
        )
