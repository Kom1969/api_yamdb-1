from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Genre, Title


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
