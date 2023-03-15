from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CategoryViewSet, GenreViewSet, TitleViewSet, CommentViewSet, ReviewViewSet

v1_router = DefaultRouter()

v1_router.register('categories', CategoryViewSet, basename='category')
v1_router.register('genres', GenreViewSet, basename='genre')
v1_router.register('titles', TitleViewSet, basename='title')
v1_router.register(r'^titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
                basename='comments')
v1_router.register(r'^titles/(?P<title_id>\d+)/comments', CommentViewSet,
                basename='comments')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    # path('v1/', include('djoser.urls')),
    # path('v1/', include('djoser.urls.jwt')),
]
