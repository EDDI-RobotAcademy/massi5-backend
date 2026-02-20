"""Reports 도메인 요청/응답 스키마."""

from datetime import date
from typing import List

from pydantic import BaseModel, Field


class ReportSummary(BaseModel):
    """리포트 요약 (기간별 점심 기록 수 등)."""

    start_date: date
    end_date: date
    total_records: int = Field(..., description="기간 내 점심 기록 수")


class ReportResponse(BaseModel):
    """리포트 응답."""

    summary: ReportSummary
    # 필요 시 상세 목록 등 확장
