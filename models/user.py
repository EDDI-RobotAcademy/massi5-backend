"""User 테이블 (Kakao 로그인 사용자)."""

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """모모고쏘 사용자. Kakao OAuth 연동."""

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    kakao_id: int = Field(unique=True, index=True, description="Kakao 사용자 ID")
    email: Optional[str] = Field(default=None, max_length=255)
    nickname: Optional[str] = Field(default=None, max_length=100)
    profile_image_url: Optional[str] = Field(default=None, max_length=512)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
