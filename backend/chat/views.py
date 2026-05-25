import logging
from django.views.generic import View
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from chat.services.llm_service import get_chat_response
from .serializers import ChatRequestSerializer, ChatResponseSerializer

logger = logging.getLogger(__name__)

class HealthCheckView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        return Response({
            "status": "ok",
            "model": "llama-3.3-70b-versatile"
        })


class ChatView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    @swagger_auto_schema(
        request_body=ChatRequestSerializer,
        responses={200: ChatResponseSerializer}
    )

    def post(self, request):

        serializer = ChatRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        messages = serializer.validated_data["messages"]
        response = get_chat_response(messages)

        return Response({"reply": response})

