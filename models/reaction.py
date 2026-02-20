"""Reaction 테이블 (점심 기록에 대한 반응)."""

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Reaction(SQLModel, table=True):
    """점심 기록에 대한 반응 (좋아요 등)."""

    __tablename__ = "reactions"

    id: Optional[int] = Field(default=None, primary_key=True)
    lunch_record_id: int = Field(foreign_key="lunch_records.id", index=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    reaction_type: str = Field(max_length=50, description="예: like, emoji 등")
    created_at: datetime = Field(default_factory=datetime.utcnow)
