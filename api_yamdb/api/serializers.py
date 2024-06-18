from rest_framework import serializers

from reviews.models import Title


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title."""

    class Meta:
        fields = '__all__'
        model = Title
