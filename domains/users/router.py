"""Users FastAPI 라우터. Controller에 의존하며 DB 세션은 Depends(get_db)로 주입."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import get_db
from domains.users.controller.user_controller import UserController
from domains.users.schemas import UserResponse
from domains.users.service.user_service_impl import UserServiceImpl


def get_controller(db: Session = Depends(get_db)) -> UserController:
    """Controller 의존성. Service 구현체와 DB 세션을 주입."""
    service = UserServiceImpl()
    return UserController(service=service, db=db)


router = APIRouter()


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
