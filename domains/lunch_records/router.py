"""Lunch records FastAPI 라우터. DB 세션은 Depends(get_db)로 주입."""

from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from core.database import get_db
from domains.lunch_records.controller.lunch_record_controller import LunchRecordController
from domains.lunch_records.schemas import (
    LunchRecordCalendarResponse,
    LunchRecordCreate,
    LunchRecordDateGroupResponse,
    LunchRecordResponse,
    LunchRecordTodayResponse,
)
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


@router.get("/today", response_model=LunchRecordTodayResponse, summary="오늘의 점심 기록 조회")
def get_today_lunch_records(
    controller: LunchRecordController = Depends(get_controller),
    # TODO: 인증 후 user_id는 JWT 등에서 추출
    user_id: int = 1,
) -> LunchRecordTodayResponse:
    """홈 화면용 오늘의 점심 기록을 조회합니다."""
    return controller.get_today(user_id=user_id)


@router.get(
    "/by-date",
    response_model=LunchRecordDateGroupResponse,
    summary="특정 날짜 점심 기록 조회",
)
def get_lunch_records_by_date(
    target_date: date = Query(..., description="조회할 날짜 (YYYY-MM-DD)"),
    controller: LunchRecordController = Depends(get_controller),
    # TODO: 인증 후 user_id는 JWT 등에서 추출
    user_id: int = 1,
) -> LunchRecordDateGroupResponse:
    """달력 날짜 클릭 시 해당 날짜의 점심 기록을 조회합니다."""
    return controller.get_by_date(user_id=user_id, target_date=target_date)


@router.get(
    "/calendar",
    response_model=LunchRecordCalendarResponse,
    summary="달력 뷰용 월별 점심 기록 집계",
)
def get_lunch_calendar(
    year: int = Query(..., ge=2000, le=2100, description="조회 연도"),
    month: int = Query(..., ge=1, le=12, description="조회 월"),
    controller: LunchRecordController = Depends(get_controller),
    # TODO: 인증 후 user_id는 JWT 등에서 추출
    user_id: int = 1,
) -> LunchRecordCalendarResponse:
    """달력 마킹을 위한 월별 날짜 집계를 조회합니다."""
    return controller.get_calendar(user_id=user_id, year=year, month=month)
