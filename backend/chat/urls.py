from django.urls import path
from .views import ChatView, SessionCreateView

urlpatterns = [
    path('v1/chat/', ChatView.as_view(), name='chat'),
    path('v1/session/create/', SessionCreateView.as_view(), name='session_create'),
]


