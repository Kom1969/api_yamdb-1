from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, GenreViewSet, TitleViewSet

router = DefaultRouter()

router.register('categories', CategoryViewSet, basename='category')
router.register('genres', GenreViewSet, basename='genre')
router.register('titles', TitleViewSet, basename='title')

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.jwt')),
]
