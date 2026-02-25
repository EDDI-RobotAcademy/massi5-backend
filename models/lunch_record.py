"""LunchRecord 테이블 (점심 기록)."""

from datetime import date, datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class LunchRecord(SQLModel, table=True):
    """점심 기록. 사용자별 식사 정보."""

    __tablename__ = "lunch_records"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    photo_url: Optional[str] = Field(default=None, max_length=512, description="음식 사진 주소")
    menu_name: str = Field(max_length=100, description="메뉴 이름")
    category: str = Field(max_length=50, description="음식 종류 (한식, 일식 등)")
    meal_type: str = Field(max_length=50, description="식사 유형 (배달, 외식 등)")
    rating: int = Field(ge=1, le=5, description="만족도 (별점)")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="기록 시간")

    # 기존 reports 도메인의 기간 집계 호환성을 위해 유지
    recorded_at: date = Field(default_factory=date.today, index=True, description="기록 날짜")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="레거시 호환용 수정 시각")
