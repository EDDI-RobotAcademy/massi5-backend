"""Lunch records Service 구현체."""

from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from domains.lunch_records.schemas import (
    LunchRecordCalendarDay,
    LunchRecordCalendarResponse,
    LunchRecordCreate,
    LunchRecordDateGroupResponse,
    LunchRecordResponse,
    LunchRecordTodayResponse,
)
from domains.lunch_records.service.lunch_record_service import LunchRecordServiceInterface
from models import LunchRecord


class LunchRecordServiceImpl(LunchRecordServiceInterface):
    def create(
        self, db: Session, user_id: int, data: LunchRecordCreate
    ) -> LunchRecordResponse:
        record = LunchRecord(
            user_id=user_id,
            recorded_at=data.recorded_at,
            photo_url=data.photo_url,
            menu_name=data.menu_name,
            category=data.category,
            meal_type=data.meal_type,
            rating=data.rating,
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return LunchRecordResponse(
            id=record.id,
            user_id=record.user_id,
            recorded_at=record.recorded_at,
            photo_url=record.photo_url,
            menu_name=record.menu_name,
            category=record.category,
            meal_type=record.meal_type,
            rating=record.rating,
            created_at=record.created_at,
        )

    def get_today(self, db: Session, user_id: int) -> LunchRecordTodayResponse:
        today = date.today()
        records = self._list_records_by_date(db=db, user_id=user_id, target_date=today)
        return LunchRecordTodayResponse(
            date=today,
            has_record=len(records) > 0,
            count=len(records),
            records=records,
        )

    def get_by_date(
        self, db: Session, user_id: int, target_date: date
    ) -> LunchRecordDateGroupResponse:
        records = self._list_records_by_date(db=db, user_id=user_id, target_date=target_date)
        return LunchRecordDateGroupResponse(date=target_date, count=len(records), records=records)

    def get_calendar(
        self, db: Session, user_id: int, year: int, month: int
    ) -> LunchRecordCalendarResponse:
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1)
        else:
            end_date = date(year, month + 1, 1)

        stmt = (
            select(LunchRecord.recorded_at, func.count(LunchRecord.id))
            .where(LunchRecord.user_id == user_id)
            .where(LunchRecord.recorded_at >= start_date)
            .where(LunchRecord.recorded_at < end_date)
            .group_by(LunchRecord.recorded_at)
            .order_by(LunchRecord.recorded_at.asc())
        )
        rows = db.execute(stmt).all()
        days = [LunchRecordCalendarDay(date=row[0], count=int(row[1])) for row in rows]
        return LunchRecordCalendarResponse(year=year, month=month, days=days)

    def _list_records_by_date(
        self, db: Session, user_id: int, target_date: date
    ) -> list[LunchRecordResponse]:
        stmt = (
            select(LunchRecord)
            .where(LunchRecord.user_id == user_id)
            .where(LunchRecord.recorded_at == target_date)
            .order_by(LunchRecord.created_at.desc())
        )
        rows = db.execute(stmt).scalars().all()
        return [
            LunchRecordResponse(
                id=record.id,
                user_id=record.user_id,
                recorded_at=record.recorded_at,
                photo_url=record.photo_url,
                menu_name=record.menu_name,
                category=record.category,
                meal_type=record.meal_type,
                rating=record.rating,
                created_at=record.created_at,
            )
            for record in rows
        ]
