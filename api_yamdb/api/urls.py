from django.urls import include, path
from rest_framework import routers


v1_router = routers.DefaultRouter()
# Дописать урлы.

urlpatterns = [
    # path('v1/', include('djoser.urls')),  # Переделаю
    # path('v1/', include('djoser.urls.jwt')),  # Переделаю
    path('v1/', include(v1_router.urls)),
]
