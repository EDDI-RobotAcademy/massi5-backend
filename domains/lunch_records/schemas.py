"""Lunch records 도메인 요청/응답 스키마."""

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class LunchRecordCreate(BaseModel):
    """점심 기록 생성 요청."""

    recorded_at: date = Field(..., description="기록 날짜")
    photo_url: Optional[str] = Field(default=None, max_length=512, description="음식 사진 주소")
    menu_name: str = Field(..., max_length=100, description="메뉴 이름")
    category: str = Field(..., max_length=50, description="음식 종류")
    meal_type: str = Field(..., max_length=50, description="식사 유형")
    rating: int = Field(..., ge=1, le=5, description="만족도 (별점)")


class LunchRecordResponse(BaseModel):
    """점심 기록 응답."""

    id: int
    user_id: int
    recorded_at: date
    photo_url: Optional[str] = None
    menu_name: str
    category: str
    meal_type: str
    rating: int
    created_at: datetime

    class Config:
        from_attributes = True


class LunchRecordDateGroupResponse(BaseModel):
    """특정 날짜 점심 기록 조회 응답."""

    date: date
    count: int
    records: list[LunchRecordResponse]


class LunchRecordTodayResponse(BaseModel):
    """홈 화면의 오늘 기록 조회 응답."""

    date: date
    has_record: bool
    count: int
    records: list[LunchRecordResponse]


class LunchRecordCalendarDay(BaseModel):
    """달력 표시용 날짜별 집계."""

    date: date
    count: int


class LunchRecordCalendarResponse(BaseModel):
    """달력 뷰 응답."""

    year: int
    month: int
    days: list[LunchRecordCalendarDay]
