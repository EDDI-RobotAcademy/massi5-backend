"""Reports Service Interface."""

from abc import ABC, abstractmethod
from datetime import date

from sqlalchemy.orm import Session

from domains.reports.schemas import ReportResponse


class ReportServiceInterface(ABC):
    @abstractmethod
    def get_period_report(
        self, db: Session, user_id: int, start_date: date, end_date: date
    ) -> ReportResponse:
        """기간별 리포트 조회."""
        ...
