"""LunchRecord 테이블 (점심 기록)."""

from datetime import date, datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class LunchRecord(SQLModel, table=True):
    """점심 기록. 사용자별 날짜·내용."""

    __tablename__ = "lunch_records"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    recorded_at: date = Field(description="기록한 날짜")
    content: Optional[str] = Field(default=None, max_length=2000, description="메모/내용")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
