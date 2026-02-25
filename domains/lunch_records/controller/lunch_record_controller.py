"""Lunch records Controller. Service에 위임하며 DB 세션을 주입받는다."""

from datetime import date

from sqlalchemy.orm import Session

from domains.lunch_records.schemas import (
    LunchRecordCalendarResponse,
    LunchRecordCreate,
    LunchRecordDateGroupResponse,
    LunchRecordResponse,
    LunchRecordTodayResponse,
)
from domains.lunch_records.service.lunch_record_service import LunchRecordServiceInterface


class LunchRecordController:
    def __init__(self, service: LunchRecordServiceInterface, db: Session) -> None:
        self._service = service
        self._db = db

    def create(self, user_id: int, body: LunchRecordCreate) -> LunchRecordResponse:
        """점심 기록 생성."""
        return self._service.create(self._db, user_id=user_id, data=body)

    def get_today(self, user_id: int) -> LunchRecordTodayResponse:
        """오늘의 점심 기록 조회."""
        return self._service.get_today(self._db, user_id=user_id)

    def get_by_date(self, user_id: int, target_date: date) -> LunchRecordDateGroupResponse:
        """특정 날짜 점심 기록 조회."""
        return self._service.get_by_date(self._db, user_id=user_id, target_date=target_date)

    def get_calendar(self, user_id: int, year: int, month: int) -> LunchRecordCalendarResponse:
        """달력 뷰용 월별 날짜 집계 조회."""
        return self._service.get_calendar(self._db, user_id=user_id, year=year, month=month)
