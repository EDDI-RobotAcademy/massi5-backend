"""Reports FastAPI 라우터. DB 세션은 Depends(get_db)로 주입."""

from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from core.database import get_db
from domains.reports.controller.report_controller import ReportController
from domains.reports.schemas import ReportResponse
from domains.reports.service.report_service_impl import ReportServiceImpl


def get_controller(db: Session = Depends(get_db)) -> ReportController:
    """Controller 의존성. Service 구현체와 DB 세션을 주입."""
    service = ReportServiceImpl()
    return ReportController(service=service, db=db)


router = APIRouter()


@router.get("/period", response_model=ReportResponse, summary="기간별 리포트")
def get_period_report(
    start_date: date = Query(..., description="시작일"),
    end_date: date = Query(..., description="종료일"),
    controller: ReportController = Depends(get_controller),
    # TODO: 인증 후 user_id는 JWT 등에서 추출
    user_id: int = 1,
) -> ReportResponse:
    """지정 기간의 점심 기록 리포트를 반환합니다."""
    return controller.get_period_report(
        user_id=user_id, start_date=start_date, end_date=end_date
    )
