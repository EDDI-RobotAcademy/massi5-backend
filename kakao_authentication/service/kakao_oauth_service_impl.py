"""Kakao OAuth Service 구현체. 환경 변수(.env) 기반으로 설정을 로드한다."""

import os
from urllib.parse import urlencode

import httpx

from kakao_authentication.schemas import AccessTokenResponse, KakaoUserInfo, OAuthLinkResponse
from kakao_authentication.service.kakao_oauth_service import KakaoAuthServiceInterface

# Kakao OAuth 상수 (코드에 하드코딩되는 것은 엔드포인트 URL만 해당)
KAKAO_AUTH_URL = "https://kauth.kakao.com/oauth/authorize"
KAKAO_TOKEN_URL = "https://kauth.kakao.com/oauth/token"
KAKAO_USER_ME_URL = "https://kapi.kakao.com/v2/user/me"


class KakaoOAuthServiceImpl(KakaoAuthServiceInterface):
    """Kakao OAuth 서비스 구현체. client_id, redirect_uri, client_secret은 환경 변수에서 로드."""

    def __init__(self) -> None:
        self._client_id = os.getenv("KAKAO_CLIENT_ID")
        self._redirect_uri = os.getenv("KAKAO_REDIRECT_URI")
        self._client_secret = os.getenv("KAKAO_CLIENT_SECRET")

    def _validate_oauth_config(self) -> None:
        """OAuth 필수 설정값 검증. 누락 시 예외."""
        if not self._client_id:
            raise ValueError("KAKAO_CLIENT_ID가 설정되지 않았습니다.")
        if not self._redirect_uri:
            raise ValueError("KAKAO_REDIRECT_URI가 설정되지 않았습니다.")

    def get_authorization_url(self) -> OAuthLinkResponse:
        """Kakao OAuth 인증 URL 생성 (PM-JIHYUN-2). client_id, redirect_uri, response_type 포함."""
        self._validate_oauth_config()
        params = {
            "client_id": self._client_id,
            "redirect_uri": self._redirect_uri,
            "response_type": "code",
        }
        auth_url = f"{KAKAO_AUTH_URL}?{urlencode(params)}"
        return OAuthLinkResponse(
            auth_url=auth_url,
            client_id=self._client_id,
            redirect_uri=self._redirect_uri,
            response_type="code",
        )

    def request_access_token(self, code: str) -> AccessTokenResponse:
        """인가 코드로 액세스 토큰 요청 후, 사용자 정보까지 조회하여 반환 (PM-JIHYUN-3, PM-JIHYUN-4)."""
        self._validate_oauth_config()
        if not self._client_secret:
            raise ValueError("KAKAO_CLIENT_SECRET이 설정되지 않았습니다.")
        if not code or not code.strip():
            raise ValueError("인가 코드(code)가 필요합니다.")

        data = {
            "grant_type": "authorization_code",
            "client_id": self._client_id,
            "redirect_uri": self._redirect_uri,
            "code": code.strip(),
            "client_secret": self._client_secret,
        }

        with httpx.Client() as client:
            token_res = client.post(
                KAKAO_TOKEN_URL,
                headers={"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"},
                data=data,
            )
            token_res.raise_for_status()
            token_body = token_res.json()

        access_token = token_body.get("access_token")
        if not access_token:
            raise ValueError("액세스 토큰을 받지 못했습니다.")

        # PM-JIHYUN-4: 발급된 액세스 토큰으로 사용자 정보 조회 후 함께 반환
        user_info = self.get_user_info(access_token)

        return AccessTokenResponse(
            access_token=access_token,
            token_type=token_body.get("token_type", "bearer"),
            refresh_token=token_body.get("refresh_token"),
            expires_in=token_body.get("expires_in"),
            refresh_token_expires_in=token_body.get("refresh_token_expires_in"),
            scope=token_body.get("scope"),
            user=user_info,
        )

    def get_user_info(self, access_token: str) -> KakaoUserInfo:
        """액세스 토큰으로 Kakao 사용자 정보 조회 (PM-JIHYUN-4)."""
        if not access_token or not access_token.strip():
            raise ValueError("액세스 토큰이 필요합니다.")

        with httpx.Client() as client:
            res = client.get(
                KAKAO_USER_ME_URL,
                headers={
                    "Authorization": f"Bearer {access_token.strip()}",
                    "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
                },
            )
            res.raise_for_status()
            body = res.json()

        kakao_account = body.get("kakao_account") or {}
        profile = kakao_account.get("profile") or {}
        return KakaoUserInfo(
            id=body.get("id"),
            nickname=profile.get("nickname"),
            email=kakao_account.get("email"),
            profile_image_url=profile.get("profile_image_url"),
        )
