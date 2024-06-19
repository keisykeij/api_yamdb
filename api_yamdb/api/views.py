from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .mixins import BaseMixinSet
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer
from reviews.models import Category, Genre, Title


class TitleViewSet(ModelViewSet):
    """ViewSet для работы с произведениями."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


class CategoryViewSet(BaseMixinSet):
    """ViewSet для работы с категиориями."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(BaseMixinSet):
    """ViewSet для работы с жанрами."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
