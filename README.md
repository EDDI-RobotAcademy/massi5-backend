# massi5-backend

모모고쏘(점심 기록 서비스) 백엔드 API.

## 환경 변수 (.env)

프로젝트 루트에 `.env` 파일을 두고 아래 항목을 설정하세요.  
예시는 `.env.example`을 참고하면 됩니다.

| 변수 | 설명 |
|------|------|
| `KAKAO_CLIENT_ID` | Kakao REST API 키 |
| `KAKAO_REDIRECT_URI` | Kakao 로그인 후 리다이렉트 URL |
| `KAKAO_CLIENT_SECRET` | Kakao Client Secret (토큰 발급 시 사용) |
| **`DATABASE_URL`** | **PostgreSQL 연결 문자열** (`postgresql://사용자:비밀번호@호스트:포트/DB이름`) |

- **DATABASE_URL**이 없으면 기본값 `postgresql://postgres:postgres@localhost:5432/massi5` 가 사용됩니다.
- DB를 먼저 생성한 뒤 서버를 실행하면, 앱 시작 시 `User`, `LunchRecord`, `Reaction` 테이블이 자동 생성됩니다.

## 실행

```bash
pip install -r requirements.txt
python3 -m main
```

API 문서: http://localhost:8000/docs
