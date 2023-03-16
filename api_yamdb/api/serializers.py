import uuid

from django.core.mail import send_mail
from rest_framework import serializers, exceptions
from rest_framework.relations import SlugRelatedField
from django.conf import settings
from reviews.models import Category, Genre, Title, Review, Comment
from users.models import User, ROLES


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'
        # read_only_fields = ('__all__', )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        # read_only_fields = ('__all__', )


class TitleSerializer(serializers.ModelSerializer):
    # genre = SlugRelatedField(
    #     slug_field='slug',
    #     read_only=True,
    #     many=True)
    # category = SlugRelatedField(slug_field='slug', read_only=True)
    category = CategorySerializer()
    genre = GenreSerializer(many=True)

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        model = Title
        # read_only_fields = ('__all__', )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('post',)


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
        if rate < settings.RATE_ONE or rate > settings.RATE_TEN:
            raise serializers.ValidationError(
                'Рейтинг произведения должен быть от 1 до 10')
        return rate


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


class UserSelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')
        read_only_fields = ('username', 'email', 'role')


class AdminUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

    def create(self, validated_data):
        confirmation_code = str(uuid.uuid4())
        if validated_data['username'] == 'me':
            error = {'username': ['Нельзя создать пользователя с username me']}
            raise exceptions.ValidationError(error)
        user = User.objects.create_user(
            confirmation_code=confirmation_code, **validated_data)
        send_mail(
            subject='Код подтверждения для YAMDB',
            message=confirmation_code,
            from_email="admin@admin.ru",
            recipient_list=[validated_data.get('email')]
        )
        user.save()
        return user


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
