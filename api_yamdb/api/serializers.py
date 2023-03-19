from django.db.models import Avg
from django.conf import settings
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api.validators import (username_validator,
                            signup_validator,
                            score_validator,
                            year_validator)
from reviews.models import Category, Genre, Title, Review, Comment
from users.models import User


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id', )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id', )


class ObjectField(serializers.SlugRelatedField):

    def to_representation(self, obj):
        return {'name': obj.name,
                'slug': obj.slug}


class TitleCreateSerializer(serializers.ModelSerializer):
    genre = ObjectField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = ObjectField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )

    class Meta:
        model = Title
        fields = '__all__'
        validators = [year_validator]


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    @staticmethod
    def get_rating(self):
        rating = self.reviews.aggregate(Avg('score')).get('score__avg')
        return round(rating, settings.RATING_ACCURACY)

    class Meta:
        fields = '__all__'
        model = Title


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Review
        validators = [score_validator]

    # Не могу допереть, как эту валидацию
    # правильно перенести в validators.py
    # из-за self
    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
#
        title_id = self.context['view'].kwargs.get('title_id')
        author = self.context['request'].user
        if Review.objects.filter(
                author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'Отзыв уже существует,'
                'допустимо не более 1 отзыва на произведение.'
            )
        return data


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=settings.USERNAME_MAX_LENGTH,
        required=True,
        validators=[
            username_validator,
            UniqueValidator(queryset=User.objects.all()),
        ]
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
        validators = [signup_validator]


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )
