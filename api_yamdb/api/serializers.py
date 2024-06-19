from rest_framework import serializers

from reviews.models import Category, Title


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title."""

    class Meta:
        fields = '__all__'
        model = Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id', )
        model = Category
