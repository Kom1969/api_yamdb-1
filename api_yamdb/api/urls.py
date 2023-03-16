from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CategoryViewSet, GenreViewSet, TitleViewSet, CommentViewSet, ReviewViewSet, UserViewSet, SignUpAPIView, MyTokenObtainPairView, UserSelfView

v1_router = DefaultRouter()

v1_router.register('categories', CategoryViewSet, basename='category')
v1_router.register('genres', GenreViewSet, basename='genre')
v1_router.register('titles', TitleViewSet, basename='title')
v1_router.register(r'^titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
                   basename='comments')
v1_router.register(r'^titles/(?P<title_id>\d+)/comments', CommentViewSet,
                   basename='comments')
v1_router.register('users',
                   UserViewSet,
                   basename='users')

urlpatterns = [
    path('v1/auth/signup/', SignUpAPIView.as_view(), name='signup'),
    path('v1/auth/token/', MyTokenObtainPairView.as_view(), name='token'),
    path('v1/users/me', UserSelfView.as_view(), name='user_self'),
    path('v1/', include(v1_router.urls)),
]
