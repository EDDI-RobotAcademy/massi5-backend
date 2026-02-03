"""환경 변수 로딩 책임을 갖는 config 모듈. 애플리케이션 시작 시 .env 파일을 1회 로드한다."""

from pathlib import Path

from dotenv import load_dotenv


def load_env() -> None:
    """
    .env 파일을 1회 로드한다.
    Service 및 Controller에서는 이 함수를 호출하지 않고,
    애플리케이션 엔트리포인트에서만 호출한다.
    """
    env_path = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(dotenv_path=env_path)
