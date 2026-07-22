# FastAPI LLM API Mini Project

FastAPI로 구성한 간단한 백엔드 예제입니다. Google Gemini를 호출하는 채팅 API와 상품 생성/조회 API를 제공하며, 라우터별 `pytest` 테스트를 포함합니다.

## 주요 기능

- Gemini 단일 채팅 요청
- 상품 생성
- 상품 단건 조회
- 상품 전체 조회
- Pydantic을 이용한 요청 및 응답 데이터 검증
- FastAPI `TestClient`를 이용한 라우터 테스트
- 외부 Gemini API를 호출하지 않는 mock 테스트

## 프로젝트 구조

```text
00_mini_project/
├─ app/
│  ├─ core/
│  │  └─ chat_config.py
│  ├─ routers/
│  │  ├─ chat_router.py
│  │  └─ product_router.py
│  ├─ schemas/
│  │  ├─ chat_schema.py
│  │  └─ product_schema.py
│  ├─ services/
│  │  ├─ chat_service.py
│  │  └─ product_service.py
│  └─ main.py
├─ test/
│  ├─ test_chat_router.py
│  └─ test_product_router.py
└─ README.md
```

라우터는 HTTP 요청을 받고, 스키마는 데이터 형식을 정의하며, 서비스는 실제 비즈니스 로직을 담당합니다.

## 실행 환경

- Python 3.10 이상
- FastAPI
- Uvicorn
- Google Gen AI SDK
- python-dotenv
- pytest
- HTTPX

가상환경을 만든 후 필요한 패키지를 설치합니다.

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install fastapi uvicorn google-genai python-dotenv pytest httpx
```

macOS/Linux:

```bash
source .venv/bin/activate
python -m pip install fastapi uvicorn google-genai python-dotenv pytest httpx
```

## 환경변수 설정

Gemini API 호출에는 API 키가 필요합니다.

현재 `app/core/chat_config.py`는 이 프로젝트 폴더에서 두 단계 위에 있는 `.env` 파일을 읽습니다.

```dotenv
GEMINI_API_KEY=your_api_key
GEMINI_MODEL=gemini-2.5-flash-lite
```

`GEMINI_MODEL`을 생략하면 `gemini-2.5-flash-lite`가 사용됩니다. 실제 API 키가 포함된 `.env` 파일은 Git에 커밋하지 않는 것을 권장합니다.

## 서버 실행

프로젝트 루트에서 다음 명령을 실행합니다.

```bash
uvicorn app.main:app --reload
```

서버가 실행되면 다음 문서 페이지에서 API를 확인하고 직접 호출할 수 있습니다.

- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>

## API 목록

| Method | Endpoint | 설명 |
|---|---|---|
| `POST` | `/chat/gemini` | Gemini에 프롬프트를 전달하고 답변을 받습니다. |
| `POST` | `/product/create` | 상품을 생성합니다. |
| `GET` | `/product/get/{product_id}` | ID로 상품 한 개를 조회합니다. |
| `GET` | `/product/getall` | 전체 상품을 조회합니다. |

### Gemini 채팅 예시

요청:

```bash
curl -X POST http://127.0.0.1:8000/chat/gemini \
  -H "Content-Type: application/json" \
  -d '{"user_id":"id01","prompt":"FastAPI를 간단히 설명해줘"}'
```

응답 예시:

```json
{
  "answer": "FastAPI는 Python으로 API를 개발하기 위한 웹 프레임워크입니다."
}
```

### 상품 생성 예시

```bash
curl -X POST http://127.0.0.1:8000/product/create \
  -H "Content-Type: application/json" \
  -d '{"id":200,"name":"shirt01","price":25000}'
```

### 상품 조회 예시

```bash
curl http://127.0.0.1:8000/product/get/100
curl http://127.0.0.1:8000/product/getall
```

## 테스트

전체 테스트를 실행합니다.

```bash
python -m pytest test -v
```

라우터별로 실행할 수도 있습니다.

```bash
python -m pytest test/test_chat_router.py -v
python -m pytest test/test_product_router.py -v
```

채팅 라우터 테스트는 Gemini 호출 함수를 mock으로 교체하므로 API 키나 네트워크 연결 없이 실행할 수 있습니다. 상품 라우터 테스트는 생성, 단건 조회, 전체 조회 및 잘못된 ID 검증을 확인합니다.

## 참고 사항

현재 상품 서비스는 데이터베이스 대신 고정된 예제 데이터를 반환합니다. 실제 프로젝트에서는 서비스 계층을 데이터베이스 저장소와 연결하도록 확장할 수 있습니다.
