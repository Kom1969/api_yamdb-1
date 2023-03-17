import uuid

from django.db.models import Avg
from django.core.mail import send_mail
from rest_framework import serializers, exceptions
from rest_framework.relations import SlugRelatedField
from django.conf import settings
from reviews.models import Category, Genre, Title, Review, Comment
from users.models import User, ROLES


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class ObjectField(serializers.SlugRelatedField):

    def to_representation(self, obj):
        return {'name': obj.name,
                'slug': obj.slug}


class TitleCreateSerializer(serializers.ModelSerializer):
    '''
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    '''
    genre = ObjectField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = ObjectField(
        slug_field='slug',
        queryset=Category.objects.all(),
        # many=False
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        model = Title

    @staticmethod
    def get_rating(obj):
        rating = obj.reviews.aggregate(Avg('rate')).get('rate__avg')
        if rating is None:
            return rating
        return round(rating, 1)


class CommentSerializer(serializers.ModelSerializer):
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

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data

        title_id = self.context['view'].kwargs.get('title_id')
        author = self.context['request'].user
        if Review.objects.filter(
                author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'Отзыв уже существует,'
                'допустимо не более 1 отзыва на произведение.'
            )
        return data

    def validate_rate(self, rate):
        if rate < 1 or rate > 10:
            raise serializers.ValidationError(
                'Рейтинг произведения должен быть от 1 до 10')
        return rate


# В процессе.
class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=ROLES, default='user')

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')

    def create(self, validated_data):
        if validated_data['username'] == 'me':
            error = {'username': ['Нельзя создать пользователя с username me']}
            raise exceptions.ValidationError(error)
        return super().create(validated_data)


# В процессе.
class UserSelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')
        read_only_fields = ('username', 'email', 'role')


# В процессе.
class AdminUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )


# В процессе.
class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

    def create(self, validated_data):
        if validated_data['username'] == 'me':
            error = {'username': ['Нельзя создать пользователя с username me']}
            raise exceptions.ValidationError(error)
        user = User.objects.create_user(**validated_data)
        send_mail(
            subject='Код подтверждения для YAMDB',
            message='123',
            from_email="admin@admin.ru",
            recipient_list=[validated_data.get('email')]
        )
        user.save()
        return user


# В процессе.
class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
