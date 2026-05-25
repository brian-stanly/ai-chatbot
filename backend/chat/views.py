import json
import logging
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from chat.services.llm_service import get_chat_response
from .serializers import MessageSerializer as SchemaMessage

logger = logging.getLogger(__name__)


def root(request):
    """Root endpoint for Django backend."""
    return JsonResponse({
        "message": "AI Chatbot API is running",
        "docs": "/api/docs",
        "health": "/api/v1/health",
    })


def health_check(request):
    """Simple health check endpoint."""
    return JsonResponse({
        "status": "ok",
        "model": "llama-3.3-70b-versatile"
    })


@csrf_exempt
async def chat(request):
    """
    Send a message to the chatbot and receive a response.
    Supports both Angular frontend format ('product') and list-of-messages format ('messages').
    """
    if request.method != 'POST':
        return JsonResponse({"detail": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        return JsonResponse({"detail": "Invalid JSON payload"}, status=400)

    messages = []
    if "product" in data:
        product_desc = data.get("product")
        if not product_desc:
            return JsonResponse({"detail": "Product description is empty"}, status=400)
        messages.append(SchemaMessage(role="user", content=f"Brainstorm brand names for: {product_desc}"))
    elif "messages" in data:
        raw_messages = data.get("messages", [])
        for msg in raw_messages:
            messages.append(SchemaMessage(
                role=msg.get("role", "user"),
                content=msg.get("content", "")
            ))
    else:
        return JsonResponse(
            {"detail": "Invalid request. Provide either 'product' or 'messages'."},
            status=400
        )

    try:
        # Await the async llm service
        companyName = await get_chat_response(messages=messages)
        return JsonResponse({
            "companyName": companyName,
            "reply": companyName
        })

    except RuntimeError as e:
        return JsonResponse({"detail": str(e)}, status=500)

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

        return JsonResponse({"detail": detail}, status=503)
