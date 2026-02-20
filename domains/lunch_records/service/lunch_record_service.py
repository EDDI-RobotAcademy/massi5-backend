"""Lunch records Service Interface."""

from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from domains.lunch_records.schemas import LunchRecordCreate, LunchRecordResponse


class LunchRecordServiceInterface(ABC):
    @abstractmethod
    def create(
        self, db: Session, user_id: int, data: LunchRecordCreate
    ) -> LunchRecordResponse:
        """점심 기록 생성."""
        ...
