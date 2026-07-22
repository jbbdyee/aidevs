from fastapi import APIRouter
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.chat_service import call_gemini

chat_router = APIRouter()

@chat_router.post("/chat/gemini")
def chat_gemini(chat_request:ChatRequest)-> ChatResponse:
    print(chat_request.user_id)
    print(chat_request.prompt)
    return call_gemini(chat_request)

