"""Users 도메인 요청/응답 스키마."""

from typing import Optional

from pydantic import BaseModel, Field


class UserResponse(BaseModel):
    """사용자 조회 응답 (공개용)."""

    id: int
    kakao_id: int
    email: Optional[str] = None
    nickname: Optional[str] = None
    profile_image_url: Optional[str] = None

    class Config:
        from_attributes = True


class UserRead(BaseModel):
    """마이페이지 내 정보 조회 응답 (MS-B-8)."""

    id: int
    kakao_id: int
    email: Optional[str] = None
    nickname: Optional[str] = None
    profile_image_url: Optional[str] = None
    is_lunch_alarm_on: bool = True
    is_report_alarm_on: bool = True

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """마이페이지 설정 수정 요청 (닉네임, 알림 설정)."""

    nickname: Optional[str] = Field(None, max_length=100, description="닉네임")
    is_lunch_alarm_on: Optional[bool] = Field(None, description="점심 알림 ON/OFF")
    is_report_alarm_on: Optional[bool] = Field(None, description="리포트 알림 ON/OFF")
