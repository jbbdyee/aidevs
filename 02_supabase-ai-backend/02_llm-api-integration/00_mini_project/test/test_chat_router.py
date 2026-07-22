from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app
from app.schemas.chat_schema import ChatResponse


client = TestClient(app)


def test_chat_gemini_returns_answer():
    with patch(
        "app.routers.chat_router.call_gemini",
        return_value=ChatResponse(answer="안녕하세요!"),
    ) as mock_call_gemini:
        response = client.post(
            "/chat/gemini",
            json={"user_id": "id01", "prompt": "안녕!"},
        )

    assert response.status_code == 200
    assert response.json() == {"answer": "안녕하세요!"}
    assert mock_call_gemini.call_args.args[0].user_id == "id01"
    assert mock_call_gemini.call_args.args[0].prompt == "안녕!"


def test_chat_gemini_rejects_empty_prompt():
    response = client.post(
        "/chat/gemini",
        json={"user_id": "id01", "prompt": ""},
    )

    assert response.status_code == 422
