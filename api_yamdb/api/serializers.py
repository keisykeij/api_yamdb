from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')

    class Meta:
        fields = ('id', 'title', 'author', 'text', 'pub_date',)
        model = Review
        read_only_fields = ('title',)

        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('title', 'author')
            )
        ]
