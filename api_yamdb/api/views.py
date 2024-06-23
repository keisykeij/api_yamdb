from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from .mixins import BaseMixinSet
from .permissions import IsAdminOrReadOnly
# from .permissions import IsAuthorOrStuffOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer)

from reviews.models import Category, Genre, Review, Title


class TitleViewSet(ModelViewSet):
    """ViewSet для работы с произведениями."""
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly, )

    def get_queryset(self):
        return Title.objects.annotate(rating=Avg('reviews__score')).all()


class CategoryViewSet(BaseMixinSet):
    """ViewSet для работы с категиориями."""
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def get_queryset(self):
        return Category.objects.all()


class GenreViewSet(BaseMixinSet):
    """ViewSet для работы с жанрами."""
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def get_queryset(self):
        return Genre.objects.all()


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    # permission_classes = (IsAuthorOrStuffOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    # permission_classes = ()
    pagination_class = PageNumberPagination

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )
