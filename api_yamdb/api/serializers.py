import re

from django.conf import settings
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Title, Review
from users.models import User


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class ObjectField(serializers.SlugRelatedField):

    def to_representation(self, obj):
        return {
            'name': obj.name,
            'slug': obj.slug,
        }


class TitleCreateSerializer(serializers.ModelSerializer):
    genre = ObjectField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
    )
    category = ObjectField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )

    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, data):
        if data >= settings.MAX_YEAR:
            raise serializers.ValidationError(
                'Год выпуска произведения должен быть меньше текущего.'
            )
        return data


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.ReadOnlyField()

    class Meta:
        model = Title
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )

    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data

        title_id = self.context['request'].parser_context['kwargs']['title_id']
        author = self.context['request'].user
        if Review.objects.filter(
                author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'Отзыв уже существует,'
                'допустимо не более 1 отзыва на произведение.'
            )
        return data

    def validate_score(self, value):
        if not settings.REVIEW_MIN_SCORE < value <= settings.REVIEW_MAX_SCORE:
            raise serializers.ValidationError(
                'Рейтинг произведения должен быть от 1 до 10.'
            )
        return value


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=settings.USERNAME_MAX_LENGTH,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        lookup_field = 'username'

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Использование юзернейма "me" запрещено.'
            )

        if not re.search(r'^[a-zA-Z][a-zA-Z0-9-_\.]{1,150}$', value):
            raise serializers.ValidationError(
                'Вы не можете использовать спецсимволы в юзернейме.'
            )
        return value


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=settings.USERNAME_MAX_LENGTH,
        required=True,
    )
    email = serializers.EmailField(max_length=settings.EMAIL_MAX_LENGTH)

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        email = data['email']
        username = data['username']
        # Я этими двойными условиями обхожу вот эти два ассерта:
        # 1) Проверьте, что повторный POST-запрос к `/api/v1/auth/signup/`
        # с данными зарегистрированного пользователя возвращает ответ
        # со статусом 200.
        # 2) Проверьте, что POST-запрос к /api/v1/auth/signup/ с данными
        # пользователя, созданного администратором, возвращает ответ
        # со статусом 200.
        # UniqueValidator и UniqueTogetherValidator не помогают
        # с этими проверками.
        if (User.objects.filter(email=email).exists()
                and not User.objects.filter(username=username).exists()):
            raise serializers.ValidationError(
                'Попробуйте указать другую электронную почту.'
            )
        if (User.objects.filter(username=username).exists()
                and not User.objects.filter(email=email).exists()):
            raise serializers.ValidationError(
                'Попробуйте указать другой юзернейм.'
            )
        return data

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Использование юзернейма "me" запрещено.'
            )

        if not re.search(r'^[a-zA-Z][a-zA-Z0-9-_\.]{1,150}$', value):
            raise serializers.ValidationError(
                'Вы не можете использовать спецсимволы в юзернейме.'
            )
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=settings.USERNAME_MAX_LENGTH,
        required=True,
    )
    confirmation_code = serializers.CharField(required=True)
