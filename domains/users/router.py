"""Users FastAPI 라우터. Controller에 의존하며 DB 세션은 Depends(get_db)로 주입."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import get_db
from domains.auth.dependencies import get_current_user
from domains.auth.schemas import AuthUserResponse
from domains.users.controller.user_controller import UserController
from domains.users.schemas import UserRead, UserResponse, UserUpdate
from domains.users.service.user_service_impl import UserServiceImpl


def get_controller(db: Session = Depends(get_db)) -> UserController:
    """Controller 의존성. Service 구현체와 DB 세션을 주입."""
    service = UserServiceImpl()
    return UserController(service=service, db=db)


router = APIRouter()


@router.get(
    "/me",
    response_model=UserRead,
    summary="내 정보 조회 (마이페이지)",
    description="[MS-B-8] 로그인한 사용자 본인의 정보를 반환합니다. JWT 필요.",
)
def get_me(
    current_user: AuthUserResponse = Depends(get_current_user),
    controller: UserController = Depends(get_controller),
) -> UserRead:
    """로그인 사용자 본인 정보 조회."""
    user = controller.get_me(current_user.id)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    return user


@router.patch(
    "/me/settings",
    response_model=UserRead,
    summary="알림 설정 및 닉네임 수정",
    description="[MS-B-8] 닉네임, 점심 알림, 리포트 알림 설정을 수정합니다. JWT 필요.",
)
def update_me_settings(
    body: UserUpdate,
    current_user: AuthUserResponse = Depends(get_current_user),
    controller: UserController = Depends(get_controller),
) -> UserRead:
    """알림 설정 및 닉네임 수정. 전달된 필드만 갱신."""
    user = controller.update_settings(current_user.id, body)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    return user


@router.get("/{user_id}", response_model=UserResponse, summary="사용자 조회")
def get_user(
    user_id: int,
    controller: UserController = Depends(get_controller),
) -> UserResponse:
    """사용자 ID로 조회."""
    user = controller.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    return user
