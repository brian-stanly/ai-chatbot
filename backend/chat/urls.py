from django.urls import path
from .views import HealthCheckView, ChatView

urlpatterns = [
    path('v1/chat/', ChatView.as_view(), name='chat'),
    path('v1/health/', HealthCheckView.as_view(), name='health_check'),
]


