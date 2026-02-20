"""Lunch records Controller. Service에 위임하며 DB 세션을 주입받는다."""

from sqlalchemy.orm import Session

from domains.lunch_records.schemas import LunchRecordCreate, LunchRecordResponse
from domains.lunch_records.service.lunch_record_service import LunchRecordServiceInterface


class LunchRecordController:
    def __init__(self, service: LunchRecordServiceInterface, db: Session) -> None:
        self._service = service
        self._db = db

    def create(self, user_id: int, body: LunchRecordCreate) -> LunchRecordResponse:
        """점심 기록 생성."""
        return self._service.create(self._db, user_id=user_id, data=body)
