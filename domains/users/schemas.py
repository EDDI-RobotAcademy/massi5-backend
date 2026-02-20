"""Users 도메인 요청/응답 스키마."""

from typing import Optional

from pydantic import BaseModel, Field


class UserResponse(BaseModel):
    """사용자 조회 응답."""

    id: int
    kakao_id: int
    email: Optional[str] = None
    nickname: Optional[str] = None
    profile_image_url: Optional[str] = None

    class Config:
        from_attributes = True
