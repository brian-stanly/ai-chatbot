from rest_framework import serializers
from typing import List, Optional
import datetime

class MessageSerializer(serializers.Serializer):
    """Serializer for a single chat message."""
    role = serializers.CharField()
    content = serializers.CharField()

# Alias to keep original import name used in services
Message = MessageSerializer

class ChatRequestSerializer(serializers.Serializer):
    """Serializer for the request payload sent to the chat endpoint."""
    messages = MessageSerializer(many=True)

class ChatResponseSerializer(serializers.Serializer):
    """Serializer for the response returned by the chat endpoint."""
    reply = serializers.CharField()

class ChatInputSerializer(serializers.Serializer):
    """Simple input serializer used for single‑message requests."""
    content = serializers.CharField()

class ConversationCreateSerializer(serializers.Serializer):
    """Serializer for creating a new conversation."""
    title = serializers.CharField(default="New Conversation", allow_blank=True, required=False)

class ConversationTitleUpdateSerializer(serializers.Serializer):
    """Serializer for updating a conversation's title."""
    title = serializers.CharField()

class ConversationResponseSerializer(serializers.Serializer):
    """Serializer for returning conversation details."""
    id = serializers.CharField()
    title = serializers.CharField()
    created_at = serializers.DateTimeField()


# Deprecated Pydantic serializer definitions removed
