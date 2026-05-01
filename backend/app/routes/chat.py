from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse, Message
from app.services.llm_service import get_chat_response

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Send a message to the chatbot and receive a response.

    - **message**: The user's current message.
    - **history**: Previous conversation messages (optional).
    """
    try:
        reply = await get_chat_response(
            history=request.history,
            user_message=request.message,
        )
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        error_msg = str(e)
        detail = "LLM service unavailable."
        
        if "403" in error_msg:
            detail = "LLM Permission Denied: Your Hugging Face token lacks sufficient permissions. Please ensure it has the 'Make calls to the serverless Inference API' permission."
        elif "429" in error_msg:
            detail = "LLM Rate Limited: Too many requests to the Hugging Face API. Please try again in a few moments."
        elif "503" in error_msg or "timeout" in error_msg.lower():
            detail = "LLM Service Unavailable: The Hugging Face model is currently loading or unavailable. Please try again soon."
        else:
            detail = f"LLM Error: {error_msg}"
            
        raise HTTPException(
            status_code=503,
            detail=detail,
        )

    # Build updated history to return to the frontend
    updated_history = list(request.history) + [
        Message(role="user", content=request.message),
        Message(role="assistant", content=reply),
    ]

    return ChatResponse(response=reply, history=updated_history)


@router.get("/health")
async def health_check():
    """Simple health check endpoint."""
    return {"status": "ok", "model": "mistralai/Mistral-7B-Instruct-v0.3"}
