from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse
from app.services.llm_service import get_chat_response

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Send a message to the chatbot and receive a response.

    - **product**: The product description.

    """
    try:

        companyName = await get_chat_response(
            messages=request.messages,
        )
        return ChatResponse(companyName=companyName)

    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    except Exception as e:
        error_msg = str(e)
                
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



@router.get("/v1/health")
async def health_check():
    """Simple health check endpoint."""
    return {"status": "ok", "model": "mistralai/Mistral-7B-Instruct-v0.3"}
