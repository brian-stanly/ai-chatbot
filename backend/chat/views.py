import logging
from django.views.generic import View
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema

from chat.services.llm_service import get_chat_response
from .serializers import (
    ChatRequestSerializer, 
    ChatResponseSerializer,
    SessionCreateSerializer
)
from .models import Message, Session

logger = logging.getLogger(__name__)

class SessionCreateView(CreateAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionCreateSerializer

class SessionListView(ListAPIView):
    queryset = Session.objects.all().order_by('-created_at')
    serializer_class = SessionCreateSerializer


class ChatView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    @swagger_auto_schema(
        request_body=ChatRequestSerializer,
        responses={200: ChatResponseSerializer}
    )

    def post(self, request):
        print("User %s", request.user)
        serializer = ChatRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        messages = serializer.validated_data["messages"]
        response = get_chat_response(messages)

        return Response({"reply": response})

