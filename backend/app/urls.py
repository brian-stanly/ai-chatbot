from django.contrib import admin
from django.urls import path, include
from chat.views import root

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', root, name='root'),
    path('api/', include('chat.urls')),
]
