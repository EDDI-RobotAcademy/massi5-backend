"""User 테이블 (Kakao 로그인 사용자)."""

from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, Column
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """모모고쏘 사용자. Kakao OAuth 연동."""

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    kakao_id: int = Field(
        sa_column=Column("kakao_id", BigInteger(), unique=True, index=True, nullable=False),
        description="Kakao 사용자 ID (21억 초과 가능)",
    )
    email: Optional[str] = Field(default=None, max_length=255)
    nickname: Optional[str] = Field(default=None, max_length=100)
    profile_image_url: Optional[str] = Field(default=None, max_length=512)
    is_lunch_alarm_on: bool = Field(default=True, description="점심 알림 ON/OFF")
    is_report_alarm_on: bool = Field(default=True, description="리포트 알림 ON/OFF")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
