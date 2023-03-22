from django.conf import settings
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Title, Review
from reviews.validators import year_validator
from users.models import User
from users.validators import username_validator


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
    year = serializers.IntegerField(
        validators=[year_validator],
    )

    class Meta:
        model = Title
        fields = '__all__'


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
        validators=[
            UniqueValidator(queryset=User.objects.all()),
            username_validator,
        ],
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


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=settings.USERNAME_MAX_LENGTH,
        required=True,
        validators=[username_validator],
    )
    email = serializers.EmailField(max_length=settings.EMAIL_MAX_LENGTH)

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        email = data['email']
        username = data['username']
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


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=settings.USERNAME_MAX_LENGTH,
        required=True,
    )
    confirmation_code = serializers.CharField(required=True)
