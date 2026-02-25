"""Lunch records Service Interface."""

from abc import ABC, abstractmethod
from datetime import date

from sqlalchemy.orm import Session

from domains.lunch_records.schemas import (
    LunchRecordCalendarResponse,
    LunchRecordCreate,
    LunchRecordDateGroupResponse,
    LunchRecordResponse,
    LunchRecordTodayResponse,
)


class LunchRecordServiceInterface(ABC):
    @abstractmethod
    def create(
        self, db: Session, user_id: int, data: LunchRecordCreate
    ) -> LunchRecordResponse:
        """점심 기록 생성."""
        ...

    @abstractmethod
    def get_today(self, db: Session, user_id: int) -> LunchRecordTodayResponse:
        """오늘의 점심 기록 조회."""
        ...

    @abstractmethod
    def get_by_date(
        self, db: Session, user_id: int, target_date: date
    ) -> LunchRecordDateGroupResponse:
        """특정 날짜의 점심 기록 조회."""
        ...

    @abstractmethod
    def get_calendar(
        self, db: Session, user_id: int, year: int, month: int
    ) -> LunchRecordCalendarResponse:
        """달력 뷰용 월별 날짜 집계 조회."""
        ...
