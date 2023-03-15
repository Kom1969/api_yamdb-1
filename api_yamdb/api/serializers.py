from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Genre, Title, Review, Comment


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
        if rate < 1 or rate > 10:
            raise serializers.ValidationError(
                'Рейтинг произведения должен быть от 1 до 10')
        return rate
