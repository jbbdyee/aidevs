from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field


app = FastAPI(title="Board CRUD API")


class PostCreate(BaseModel):
    """게시글 작성 요청 모델"""

    title: str = Field(min_length=1, max_length=100, examples=["첫 번째 글"])
    content: str = Field(min_length=1, examples=["게시글 내용입니다."])
    author: str = Field(min_length=1, max_length=30, examples=["홍길동"])


class PostUpdate(BaseModel):
    """게시글 수정 요청 모델"""

    title: str = Field(min_length=1, max_length=100, examples=["수정한 제목"])
    content: str = Field(min_length=1, examples=["수정한 내용입니다."])
    author: str = Field(min_length=1, max_length=30, examples=["홍길동"])


# 학습용 메모리 저장소입니다.
# 서버를 재시작하면 데이터가 초기화됩니다.
posts = {
    1: {
        "id": 1,
        "title": "FastAPI 게시판 시작",
        "content": "첫 번째 게시글입니다.",
        "author": "admin",
    }
}
next_post_id = 2


@app.get("/posts")
def list_posts():
    """게시글 목록 조회"""

    return {"data": list(posts.values())}


@app.get("/posts/{post_id}")
def get_post(post_id: int):
    """게시글 상세 조회"""

    if post_id not in posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    return {"data": posts[post_id]}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate):
    """게시글 작성"""

    global next_post_id

    new_post = {
        "id": next_post_id,
        "title": post.title,
        "content": post.content,
        "author": post.author,
    }
    posts[next_post_id] = new_post
    next_post_id += 1

    return {"message": "post created", "data": new_post}


@app.put("/posts/{post_id}")
def update_post(post_id: int, post: PostUpdate):
    """게시글 전체 수정"""

    if post_id not in posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    updated_post = {
        "id": post_id,
        "title": post.title,
        "content": post.content,
        "author": post.author,
    }
    posts[post_id] = updated_post

    return {"message": "post updated", "data": updated_post}


@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    """게시글 삭제"""

    if post_id not in posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    deleted_post = posts.pop(post_id)
    return {"message": "post deleted", "data": deleted_post}