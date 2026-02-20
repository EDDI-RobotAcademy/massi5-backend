"""Reports Controller. Service에 위임하며 DB 세션을 주입받는다."""

from datetime import date

from sqlalchemy.orm import Session

from domains.reports.schemas import ReportResponse
from domains.reports.service.report_service import ReportServiceInterface


class ReportController:
    def __init__(self, service: ReportServiceInterface, db: Session) -> None:
        self._service = service
        self._db = db

    def get_period_report(
        self, user_id: int, start_date: date, end_date: date
    ) -> ReportResponse:
        """기간별 리포트 조회."""
        return self._service.get_period_report(
            self._db, user_id=user_id, start_date=start_date, end_date=end_date
        )
