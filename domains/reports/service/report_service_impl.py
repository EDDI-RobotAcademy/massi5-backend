"""Reports Service 구현체."""

from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from domains.reports.schemas import ReportResponse, ReportSummary
from domains.reports.service.report_service import ReportServiceInterface
from models import LunchRecord


class ReportServiceImpl(ReportServiceInterface):
    def get_period_report(
        self, db: Session, user_id: int, start_date: date, end_date: date
    ) -> ReportResponse:
        stmt = (
            select(func.count(LunchRecord.id))
            .where(LunchRecord.user_id == user_id)
            .where(LunchRecord.recorded_at >= start_date)
            .where(LunchRecord.recorded_at <= end_date)
        )
        count = db.scalar(stmt) or 0
        summary = ReportSummary(
            start_date=start_date,
            end_date=end_date,
            total_records=count,
        )
        return ReportResponse(summary=summary)
