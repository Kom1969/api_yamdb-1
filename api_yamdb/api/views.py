import uuid
import django_filters

from django.db import IntegrityError
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import filters, viewsets, mixins, status, serializers
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView

from reviews.models import Category, Genre, Title, Review
from api.permissions import IsAdmin, IsModerator, IsAuthorOrReadOnly, ReadOnly
from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleSerializer, TitleCreateSerializer,
                             CommentSerializer,
                             ReviewSerializer, TokenSerializer,
                             SignUpSerializer, AdminUserSerializer,
                             UserSerializer, UserSelfSerializer)
from users.models import User


class TitleFilter(django_filters.FilterSet):
    genre = django_filters.CharFilter(field_name='genre__slug')
    category = django_filters.CharFilter(field_name='category__slug')
    year = django_filters.NumberFilter(field_name='year')
    name = django_filters.CharFilter(field_name='name', lookup_expr='contains')

    class Meta:
        model = Title
        fields = '__all__'


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdmin | ReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdmin | ReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdmin | ReadOnly,)
    pagination_class = LimitOffsetPagination
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH', 'PUT'):
            return TitleCreateSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdmin | IsModerator | IsAuthorOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdmin | IsModerator | IsAuthorOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


# В процессе.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = (IsAdmin,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    # lookup_value_regex = r'[\w\@\.\+\-]+'

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        url_name='me',
        permission_classes=(IsAuthenticated,)
    )
    def about(self, request):
        serializer = UserSerializer(request.user)
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)


# В процессе.
class UserSelfView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = User.objects.get(username=request.user.username)
        serializer = UserSelfSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        user = User.objects.get(username=request.user.username)
        serializer = UserSelfSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# В процессе.
class SignUpView(APIView):

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            username = serializer.validated_data['username']
            user, mail = User.objects.get_or_create(
                email=email,
                username=username
            )
            confirmation_code = default_token_generator.make_token(user)
            message = (
                f'Ваш код: {confirmation_code}\n'
                'Перейдите по адресу '
                'http://127.0.0.1:8000/api/v1/auth/token/ и введите его '
                'вместе со своим username'
            )
            send_mail(
                'Завершение регистрации',
                message,
                'webmaster@localhost',
                [email, ],
                fail_silently=True
            )
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# def signup_user(request):
#     serializer = SignUpSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#
#     email = serializer.validated_data['email']
#     username = serializer.validated_data['username']
#     try:
#         user, _ = User.objects.get_or_create(
#             email=email,
#             username=username
#         )
#     except IntegrityError:
#         raise serializers.ValidationError('Такой пользователь уже существует')
#
#     confirmation_code = default_token_generator.make_token(user)
#
#     message = (
#         f'Ваш код: {confirmation_code}\n'
#         'Перейдите по адресу '
#         'http://127.0.0.1:8000/api/v1/auth/token/ и введите его '
#         'вместе со своим username'
#     )
#
#     send_mail(
#         'Завершение регистрации',
#         message,
#         'webmaster@localhost',
#         [email, ],
#         fail_silently=True
#     )
#     return Response(
#         serializer.data,
#         status=status.HTTP_200_OK
#     )
#

class ObtainTokenView(APIView):

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            confirmation_code = serializer.validated_data['confirmation_code']
            username = serializer.validated_data['username']
            user = get_object_or_404(User, username=username)

            if default_token_generator.check_token(user, confirmation_code):
                access = AccessToken.for_user(user)
                return Response(
                    {
                        'token': f'Bearer {access}',
                    },
                    status=status.HTTP_201_CREATED
                )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

# @api_view(['POST'])
# def get_token(request):
#     serializer = TokenSerializer(data=request.data)
#     if serializer.is_valid():
#         confirmation_code = serializer.validated_data['confirmation_code']
#         username = serializer.validated_data['username']
#         user = get_object_or_404(User, username=username)
#
#         if default_token_generator.check_token(user, confirmation_code):
#             access = AccessToken.for_user(user)
#             return Response(
#                 {
#                     'token': f'Bearer {access}',
#                 },
#                 status=status.HTTP_201_CREATED
#             )
#     return Response(
#         serializer.errors,
#         status=status.HTTP_400_BAD_REQUEST
#     )
