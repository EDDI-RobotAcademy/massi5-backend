"""FastAPI 애플리케이션 엔트리포인트. 환경 변수 로딩 후 앱을 시작한다."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from config.env import load_env
from core.database import create_db_and_tables
from domains.auth.router import router as auth_router
from domains.lunch_records.router import router as lunch_records_router
from domains.reports.router import router as reports_router
from domains.users.router import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 시작 시 .env를 1회 로드하고, DB 테이블을 생성한다."""
    load_env()
    create_db_and_tables()
    yield


app = FastAPI(
    title="모모고쏘 Backend",
    description="점심 기록 서비스 API",
    lifespan=lifespan,
)

# 모든 도메인에서 DB 세션은 Depends(get_db)로 주입
# auth: Kakao OAuth (DB 미사용), 나머지: get_db 사용
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(lunch_records_router, prefix="/lunch-records", tags=["lunch-records"])
app.include_router(reports_router, prefix="/reports", tags=["reports"])


if __name__ == "__main__":
    import uvicorn

    # python3 -m main 으로 실행 (macOS에서는 python 대신 python3 사용)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
