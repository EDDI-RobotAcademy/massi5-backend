"""Lunch records FastAPI 라우터. DB 세션은 Depends(get_db)로 주입."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from domains.lunch_records.controller.lunch_record_controller import LunchRecordController
from domains.lunch_records.schemas import LunchRecordCreate, LunchRecordResponse
from domains.lunch_records.service.lunch_record_service_impl import LunchRecordServiceImpl


def get_controller(db: Session = Depends(get_db)) -> LunchRecordController:
    """Controller 의존성. Service 구현체와 DB 세션을 주입."""
    service = LunchRecordServiceImpl()
    return LunchRecordController(service=service, db=db)


router = APIRouter()


@router.post("/", response_model=LunchRecordResponse, summary="점심 기록 생성")
def create_lunch_record(
    body: LunchRecordCreate,
    controller: LunchRecordController = Depends(get_controller),
    # TODO: 인증 후 user_id는 JWT 등에서 추출
    user_id: int = 1,
) -> LunchRecordResponse:
    """점심 기록을 생성합니다."""
    return controller.create(user_id=user_id, body=body)
