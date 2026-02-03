"""Kakao 인증 관련 요청/응답 스키마."""

from typing import Optional

from pydantic import BaseModel, Field


# --- PM-JIHYUN-2: 인증 URL ---
class OAuthLinkResponse(BaseModel):
    """인증 URL 생성 API 응답 (사진1번 형태: auth_url, client_id, redirect_uri, response_type)."""
    auth_url: str = Field(..., description="Kakao OAuth 인증 페이지 URL")
    client_id: str = Field(..., description="Kakao REST API 키")
    redirect_uri: str = Field(..., description="로그인 후 리다이렉트될 콜백 URL")
    response_type: str = Field(default="code", description="OAuth response_type")


# --- PM-JIHYUN-3, PM-JIHYUN-4: 토큰 및 사용자 정보 ---
class KakaoUserInfo(BaseModel):
    """Kakao 사용자 정보 (PM-JIHYUN-4)."""
    id: int = Field(..., description="Kakao 사용자 ID")
    nickname: Optional[str] = Field(None, description="닉네임")
    email: Optional[str] = Field(None, description="이메일 (동의 시)")
    profile_image_url: Optional[str] = Field(None, description="프로필 이미지 URL")


class AccessTokenResponse(BaseModel):
    """액세스 토큰 발급 API 응답 (PM-JIHYUN-3). 리프레시 토큰 및 사용자 정보 포함 (PM-JIHYUN-4 연동)."""
    access_token: str = Field(..., description="액세스 토큰")
    token_type: str = Field(default="bearer", description="토큰 타입")
    refresh_token: Optional[str] = Field(None, description="리프레시 토큰")
    expires_in: Optional[int] = Field(None, description="액세스 토큰 만료 시간(초)")
    refresh_token_expires_in: Optional[int] = Field(None, description="리프레시 토큰 만료 시간(초)")
    scope: Optional[str] = Field(None, description="동의 항목 범위")
    user: Optional[KakaoUserInfo] = Field(None, description="Kakao 사용자 정보 (PM-JIHYUN-4)")
