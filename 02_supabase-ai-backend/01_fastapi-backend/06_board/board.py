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