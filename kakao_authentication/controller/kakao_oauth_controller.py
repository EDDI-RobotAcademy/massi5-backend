"""Kakao 인증 Controller. Service Interface에만 의존하며 요청 전달 및 응답 반환만 수행한다."""

import httpx
from fastapi import HTTPException, Query

from kakao_authentication.schemas import AccessTokenResponse, KakaoUserInfo, OAuthLinkResponse
from kakao_authentication.service.kakao_oauth_service import KakaoAuthServiceInterface


class KakaoAuthController:
    """Controller는 환경 변수, 기본값, URL 구성 로직을 다루지 않고 Service Interface에 위임한다."""

    def __init__(self, service: KakaoAuthServiceInterface) -> None:
        self._service = service

    def get_oauth_link(self) -> OAuthLinkResponse:
        """GET /kakao-authentication/request-oauth-link: 인증 URL 반환 (PM-JIHYUN-2)."""
        try:
            return self._service.get_authorization_url()
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    def request_access_token_after_redirection(
        self,
        code: str = Query(..., description="Kakao 인증 후 전달된 인가 코드"),
    ) -> AccessTokenResponse:
        """GET /kakao-authentication/request-access-token-after-redirection: 인가 코드로 토큰 발급 (PM-JIHYUN-3)."""
        try:
            return self._service.request_access_token(code=code)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except httpx.HTTPStatusError as e:
            msg = e.response.text if e.response else str(e)
            raise HTTPException(status_code=502, detail=f"Kakao 토큰 요청 실패: {msg}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_user_info(
        self,
        access_token: str = Query(..., description="Kakao 액세스 토큰"),
    ) -> KakaoUserInfo:
        """GET /kakao-authentication/user-info: 액세스 토큰으로 사용자 정보 조회 (PM-JIHYUN-4)."""
        try:
            return self._service.get_user_info(access_token=access_token)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except httpx.HTTPStatusError as e:
            msg = e.response.text if e.response else str(e)
            raise HTTPException(status_code=502, detail=f"Kakao 사용자 정보 요청 실패: {msg}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
