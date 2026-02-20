"""Kakao 인증 FastAPI 라우터. Controller에만 의존한다."""

from fastapi import APIRouter, Depends, Query
from fastapi.responses import HTMLResponse, JSONResponse

from kakao_authentication.controller.kakao_oauth_controller import KakaoAuthController
from kakao_authentication.schemas import AccessTokenResponse, KakaoUserInfo, OAuthLinkResponse
from kakao_authentication.service.kakao_oauth_service_impl import KakaoOAuthServiceImpl


def get_controller() -> KakaoAuthController:
    """Controller 의존성. Service 구현체를 주입한다."""
    service = KakaoOAuthServiceImpl()
    return KakaoAuthController(service=service)


router = APIRouter()


def _oauth_link_html(auth_url: str) -> str:
    """auth_url을 클릭 가능한 링크로 보여주는 HTML."""
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Kakao OAuth 인증 링크</title>
  <style>
    body {{ font-family: system-ui, sans-serif; max-width: 640px; margin: 2rem auto; padding: 0 1rem; }}
    h1 {{ font-size: 1.25rem; }}
    .field {{ margin: 0.75rem 0; }}
    .label {{ font-weight: 600; color: #333; }}
    a {{ color: #0066cc; text-decoration: underline; word-break: break-all; }}
    a:hover {{ color: #004499; }}
    .btn {{ display: inline-block; margin-top: 1rem; padding: 0.5rem 1rem; background: #fee500; color: #000; border-radius: 6px; text-decoration: none; font-weight: 600; }}
    .btn:hover {{ background: #fada0a; }}
  </style>
</head>
<body>
  <h1>Kakao OAuth 인증</h1>
  <div class="field">
    <span class="label">auth_url: </span>
    <a href="{auth_url}" rel="noopener noreferrer">{auth_url}</a>
  </div>
  <p><a href="{auth_url}" class="btn" rel="noopener noreferrer">Kakao 로그인</a></p>
</body>
</html>"""


def _login_success_html(nickname: str | None, email: str | None) -> str:
    """로그인 성공 시 브라우저에 보여줄 HTML."""
    name = nickname or "사용자"
    email_line = f'<p class="field">이메일: {email}</p>' if email else ""
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>로그인 성공</title>
  <style>
    body {{ font-family: system-ui, sans-serif; max-width: 480px; margin: 4rem auto; padding: 0 1rem; text-align: center; }}
    h1 {{ font-size: 1.5rem; color: #333; }}
    .field {{ margin: 0.5rem 0; color: #555; }}
    .welcome {{ margin-bottom: 1.5rem; }}
  </style>
</head>
<body>
  <h1 class="welcome">로그인 성공</h1>
  <p class="field"><strong>{name}</strong>님, 환영합니다.</p>
  {email_line}
</body>
</html>"""


@router.get(
    "/request-oauth-link",
    response_class=JSONResponse,
    summary="Kakao 인증 URL 생성",
    description="Kakao OAuth 인증 페이지로 이동할 URL 등을 JSON으로 반환합니다 (PM-JIHYUN-2). auth_url, client_id, redirect_uri, response_type 포함.",
)
def request_oauth_link(
    controller: KakaoAuthController = Depends(get_controller),
):
    """사용자가 Kakao 인증 요청 시 인증 URL 등을 반환한다. 항상 JSON (사진1번 형태)."""
    data = controller.get_oauth_link()
    return JSONResponse(content=data.model_dump())


def _login_response_json(data) -> dict:
    """로그인 성공 시 이미지와 같은 형태의 JSON: token + user_info."""
    token = {
        "access_token": data.access_token,
        "token_type": data.token_type,
        "refresh_token": data.refresh_token,
        "expires_in": data.expires_in,
        "refresh_token_expires_in": data.refresh_token_expires_in,
        "scope": data.scope,
    }
    user = data.user
    user_info = (
        {
            "id": user.id,
            "nickname": user.nickname,
            "email": user.email,
            "profile_image_url": user.profile_image_url,
        }
        if user
        else None
    )
    return {"token": token, "user_info": user_info}


@router.get(
    "/request-access-token-after-redirection",
    summary="인가 코드로 액세스 토큰 발급",
    description="Kakao 인증 후 전달된 인가 코드로 액세스 토큰 및 사용자 정보를 발급합니다 (PM-JIHYUN-3, PM-JIHYUN-4). JSON으로 token, user_info 반환.",
)
def request_access_token_after_redirection(
    code: str = Query(..., description="Kakao 인증 후 리다이렉트 시 전달된 인가 코드"),
    controller: KakaoAuthController = Depends(get_controller),
):
    """인가 코드(code)를 받아 액세스 토큰 및 사용자 정보를 요청한다. token + user_info 형태 JSON 반환."""
    data = controller.request_access_token_after_redirection(code=code)
    return JSONResponse(content=_login_response_json(data))


@router.get(
    "/user-info",
    response_model=KakaoUserInfo,
    summary="액세스 토큰으로 사용자 정보 조회",
    description="발급받은 Kakao 액세스 토큰으로 사용자 ID, 닉네임, 이메일 등을 조회합니다 (PM-JIHYUN-4).",
)
def get_user_info(
    access_token: str = Query(..., description="Kakao 액세스 토큰"),
    controller: KakaoAuthController = Depends(get_controller),
) -> KakaoUserInfo:
    """발급받은 액세스 토큰으로 Kakao 사용자 정보를 조회한다."""
    return controller.get_user_info(access_token=access_token)
