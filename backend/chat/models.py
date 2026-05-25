import uuid
from django.db import models


class Conversation(models.Model):
    id = models.CharField(primary_key=True, max_length=255, default=uuid.uuid4)
    title = models.CharField(max_length=255, default="New Conversation")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "conversations"


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages",
        db_column="converstion_id"  # match SQLAlchemy schema spelling
    )
    role = models.CharField(max_length=50, null=True, blank=True)  # user or assistant
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "messages"
