from rest_framework import filters, permissions, viewsets, mixins
from rest_framework.pagination import LimitOffsetPagination
from django.shortcuts import get_object_or_404

from reviews.models import Category, Genre, Title, Review
from api.permissions import ForAnybody, IsAuthorOrReadOnly
from api.serializers import (CategorySerializer, GenreSerializer,
                          TitleSerializer, CommentSerializer, ReviewSerializer)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (ForAnybody,)  # потом - IsAdminUser ???
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def perform_create(self, serializer):
        serializer.save()


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (ForAnybody, )  # (permissions.AllowAny,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def perform_create(self, serializer):
        serializer.save()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (ForAnybody, )
    pagination_class = LimitOffsetPagination
    # тут тоже нужен фильтр

    def perform_create(self, serializer):
        serializer.save()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
