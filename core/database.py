"""PostgreSQL 연결 및 DB 세션 관리. .env의 DATABASE_URL을 사용한다."""

import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlmodel import SQLModel

# 모델을 import하여 metadata에 테이블이 등록되도록 함
from models import LunchRecord, Reaction, User  # noqa: F401

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/massi5",
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False,  # SQL 로그 필요 시 True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_db_and_tables() -> None:
    """SQLModel 메타데이터로 테이블 생성. 앱 시작 시 호출 가능."""
    SQLModel.metadata.create_all(engine)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI Depends용 DB 세션 제너레이터.
    요청마다 세션을 생성하고 종료 시 반환한다.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
