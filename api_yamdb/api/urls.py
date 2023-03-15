from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CommentViewSet, ReviewViewSet

router = DefaultRouter()

router.register(r'^titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
                basename='comments')
router.register(r'^titles/(?P<title_id>\d+)/comments', CommentViewSet,
                basename='comments')
urlpatterns = [
    path('v1/', include(router.urls)),
]
