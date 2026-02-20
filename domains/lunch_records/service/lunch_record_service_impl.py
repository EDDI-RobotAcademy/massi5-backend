"""Lunch records Service 구현체."""

from sqlalchemy.orm import Session

from domains.lunch_records.schemas import LunchRecordCreate, LunchRecordResponse
from domains.lunch_records.service.lunch_record_service import LunchRecordServiceInterface
from models import LunchRecord


class LunchRecordServiceImpl(LunchRecordServiceInterface):
    def create(
        self, db: Session, user_id: int, data: LunchRecordCreate
    ) -> LunchRecordResponse:
        record = LunchRecord(
            user_id=user_id,
            recorded_at=data.recorded_at,
            content=data.content,
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return LunchRecordResponse(
            id=record.id,
            user_id=record.user_id,
            recorded_at=record.recorded_at,
            content=record.content,
        )
