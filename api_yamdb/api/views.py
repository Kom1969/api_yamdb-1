from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination

# Create your views here.
from reviews.models import Category, Genre, Title
from .permissions import ForAnybody
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleSerializer)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (ForAnybody,)  # потом - IsAdminUser ???
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (ForAnybody, )  # (permissions.AllowAny,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (ForAnybody, )
    pagination_class = LimitOffsetPagination
    # тут тоже нужен фильтр