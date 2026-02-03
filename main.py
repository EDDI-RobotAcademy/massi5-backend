"""FastAPI 애플리케이션 엔트리포인트. 환경 변수 로딩 후 앱을 시작한다."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from config.env import load_env
from kakao_authentication.router import router as kakao_auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 시작 시 .env를 1회 로드한다."""
    load_env()
    yield


app = FastAPI(title="Kakao Auth Backend", lifespan=lifespan)
app.include_router(kakao_auth_router, prefix="/kakao-authentication", tags=["kakao-authentication"])


if __name__ == "__main__":
    import uvicorn

    # python3 -m main 으로 실행 (macOS에서는 python 대신 python3 사용)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
