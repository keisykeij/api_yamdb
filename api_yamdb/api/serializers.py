from rest_framework import serializers

from reviews.models import (
    Comment, Category, Genre, Review, Title
)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CreateTitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        'slug', queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        'slug', many=True, queryset=Genre.objects.all()
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title."""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        read_only=True,
        many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description',
                  'genre', 'category')
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    title = serializers.PrimaryKeyRelatedField(
        read_only=True, required=False
    )

    class Meta:
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, attrs):
        title = self.context.get('title')
        author = self.context['request'].user
        request = self.context['request']

        if request.method == "POST":
            if Review.objects.filter(title=title, author=author).exists():
                raise serializers.ValidationError(
                    "Вы уже оставили отзыв для этого произведения."
                )
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')

    class Meta:
        fields = ('id', 'review', 'author', 'text', 'created')
        model = Comment
        read_only_fields = ('review',)
