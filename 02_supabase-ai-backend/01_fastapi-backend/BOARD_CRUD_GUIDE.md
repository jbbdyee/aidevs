# FastAPI 게시판 CRUD 만들기

이 문서는 `06_board/01_http-methods.py`의 HTTP Method 예제를 참고하여, 메모리 기반의 간단한 게시판 CRUD API를 만드는 방법을 설명합니다.

## 1. CRUD와 HTTP Method

| 기능 | HTTP Method | API 경로 | 설명 |
|---|---|---|---|
| 게시글 목록 조회 | `GET` | `/boards` | 모든 게시글을 조회합니다. |
| 게시글 상세 조회 | `GET` | `/boards/{board_id}` | ID에 해당하는 게시글 하나를 조회합니다. |
| 게시글 작성 | `POST` | `/boards` | 새로운 게시글을 작성합니다. |
| 게시글 수정 | `PUT` | `/boards/{board_id}` | 기존 게시글 전체를 수정합니다. |
| 게시글 삭제 | `DELETE` | `/boards/{board_id}` | 기존 게시글을 삭제합니다. |

## 2. 게시글 데이터 구조

게시글은 다음 필드를 사용합니다.

| 필드 | 타입 | 설명 |
|---|---|---|
| `id` | `int` | 게시글 고유 번호 |
| `title` | `str` | 제목 |
| `content` | `str` | 내용 |
| `author` | `str` | 작성자 |

클라이언트가 게시글을 작성하거나 수정할 때 `id`는 서버에서 관리하므로 요청 본문에 넣지 않습니다.

## 3. 전체 예제 코드

아래 코드를 `board.py`로 저장합니다.

```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field


app = FastAPI(title="Board CRUD API")


class BoardCreate(BaseModel):
    """게시글 작성 요청 모델"""

    title: str = Field(min_length=1, max_length=100, examples=["첫 번째 글"])
    content: str = Field(min_length=1, examples=["게시글 내용입니다."])
    author: str = Field(min_length=1, max_length=30, examples=["홍길동"])


class BoardUpdate(BaseModel):
    """게시글 수정 요청 모델"""

    title: str = Field(min_length=1, max_length=100, examples=["수정한 제목"])
    content: str = Field(min_length=1, examples=["수정한 내용입니다."])
    author: str = Field(min_length=1, max_length=30, examples=["홍길동"])


# 학습용 메모리 저장소입니다.
# 서버를 재시작하면 데이터가 초기화됩니다.
boards = {
    1: {
        "id": 1,
        "title": "FastAPI 게시판 시작",
        "content": "첫 번째 게시글입니다.",
        "author": "admin",
    }
}
next_board_id = 2


@app.get("/boards")
def list_boards():
    """게시글 목록 조회"""

    return {"data": list(boards.values())}


@app.get("/boards/{board_id}")
def get_board(board_id: int):
    """게시글 상세 조회"""

    if board_id not in boards:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found",
        )

    return {"data": boards[board_id]}


@app.post("/boards", status_code=status.HTTP_201_CREATED)
def create_board(board: BoardCreate):
    """게시글 작성"""

    global next_board_id

    new_board = {
        "id": next_board_id,
        "title": board.title,
        "content": board.content,
        "author": board.author,
    }
    boards[next_board_id] = new_board
    next_board_id += 1

    return {"message": "board created", "data": new_board}


@app.put("/boards/{board_id}")
def update_board(board_id: int, board: BoardUpdate):
    """게시글 전체 수정"""

    if board_id not in boards:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found",
        )

    updated_board = {
        "id": board_id,
        "title": board.title,
        "content": board.content,
        "author": board.author,
    }
    boards[board_id] = updated_board

    return {"message": "board updated", "data": updated_board}


@app.delete("/boards/{board_id}")
def delete_board(board_id: int):
    """게시글 삭제"""

    if board_id not in boards:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found",
        )

    deleted_board = boards.pop(board_id)
    return {"message": "board deleted", "data": deleted_board}
```

## 4. 설치 및 실행

FastAPI와 Uvicorn을 설치합니다.

```bash
pip install fastapi uvicorn
```

`board.py`가 있는 폴더에서 서버를 실행합니다.

```bash
python -m uvicorn board:app --reload
```

브라우저에서 다음 주소로 접속하면 Swagger UI를 이용해 각 API를 테스트할 수 있습니다.

```text
http://127.0.0.1:8000/docs
```

## 5. 요청 예시

### 게시글 작성

`POST /boards`

```json
{
  "title": "FastAPI 공부",
  "content": "게시판 CRUD를 만들고 있습니다.",
  "author": "홍길동"
}
```

성공하면 HTTP 상태 코드 `201 Created`와 생성된 게시글을 반환합니다.

### 게시글 목록 조회

`GET /boards`

요청 본문 없이 모든 게시글을 조회합니다.

### 게시글 상세 조회

`GET /boards/1`

게시글이 없으면 HTTP 상태 코드 `404 Not Found`를 반환합니다.

### 게시글 수정

`PUT /boards/1`

```json
{
  "title": "수정한 제목",
  "content": "수정한 게시글 내용입니다.",
  "author": "홍길동"
}
```

### 게시글 삭제

`DELETE /boards/1`

삭제된 게시글 정보를 응답으로 반환합니다.

## 6. 참고 파일과 달라진 점

- 리소스 이름을 `memo`에서 `board`로 변경했습니다.
- 게시글에 `author` 필드를 추가했습니다.
- REST API 경로를 명사형 `/boards`로 통일했습니다.
- 수정할 게시글 ID를 요청 본문이 아니라 `/boards/{board_id}` 경로에서 받습니다.
- 상태 코드 상수를 사용해 `404`, `201`의 의미를 더 분명하게 표현했습니다.

## 7. 다음 단계

현재 예제는 Python 딕셔너리에 게시글을 저장하므로 서버를 재시작하면 데이터가 사라집니다. 기본 CRUD 동작을 확인한 다음에는 다음 순서로 확장할 수 있습니다.

1. Supabase에 `boards` 테이블을 생성합니다.
2. 메모리 딕셔너리 대신 Supabase에서 게시글을 조회하고 저장합니다.
3. `created_at`, `updated_at` 필드를 추가합니다.
4. `PATCH`를 사용한 부분 수정 기능을 추가합니다.
5. 페이지네이션, 검색, 사용자 인증을 추가합니다.

