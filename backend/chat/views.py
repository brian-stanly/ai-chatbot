import logging
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from asgiref.sync import async_to_sync

from chat.services.llm_service import get_chat_response
from .serializers import MessageSerializer as SchemaMessage

logger = logging.getLogger(__name__)

class HealthCheckView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        return Response({
            "status": "ok",
            "model": "llama-3.3-70b-versatile"
        })

@method_decorator(csrf_exempt, name='dispatch')
class ChatView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    def post(self, request, *args, **kwargs):
        """Handle chat request, mirroring previous logic."""
        data = request.data
        messages = []
        if "product" in data:
            product_desc = data.get("product")
            if not product_desc:
                return Response({"detail": "Product description is empty"}, status=400)
            messages.append(SchemaMessage(role="user", content=f"Brainstorm brand names for: {product_desc}"))
        elif "messages" in data:
            raw_messages = data.get("messages", [])
            for msg in raw_messages:
                messages.append(SchemaMessage(
                    role=msg.get("role", "user"),
                    content=msg.get("content", "")
                ))
        else:
            return Response({"detail": "Invalid request. Provide either 'product' or 'messages'."}, status=400)
        try:
            # Call async LLM service synchronously
            company_name = async_to_sync(get_chat_response)(messages=messages)
            return Response({"companyName": company_name, "reply": company_name})
        except RuntimeError as e:
            return Response({"detail": str(e)}, status=500)
        except Exception as e:
            err = str(e)
            if "403" in err:
                detail = "LLM Permission Denied: token lacks required permission."
            elif "429" in err:
                detail = "LLM Rate Limited: too many requests."
            elif "503" in err or "timeout" in err.lower():
                detail = "LLM Service Unavailable: model loading or down."
            else:
                detail = f"LLM Error: {err}"
            return Response({"detail": detail}, status=503)
