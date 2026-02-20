"""Lunch records 도메인 요청/응답 스키마."""

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class LunchRecordCreate(BaseModel):
    """점심 기록 생성 요청."""

    recorded_at: date = Field(..., description="기록한 날짜")
    content: Optional[str] = Field(None, max_length=2000)


class LunchRecordResponse(BaseModel):
    """점심 기록 응답."""

    id: int
    user_id: int
    recorded_at: date
    content: Optional[str] = None

    class Config:
        from_attributes = True
