from django.urls import path
from . import views

urlpatterns = [
    path('v1/chat', views.chat, name='chat'),
    path('v1/health', views.health_check, name='health_check'),
]
