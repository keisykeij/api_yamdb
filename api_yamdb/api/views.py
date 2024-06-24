from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend

from .mixins import BaseMixinSet, CommmentReviewMixin
from .permissions import IsAdminOrReadOnly
from .serializers import (
    CategorySerializer, CommentSerializer, GenreSerializer,
    ReviewSerializer, TitleSerializer, CreateTitleSerializer
)
from .filters import TitleFilter

from reviews.models import Category, Genre, Review, Title


class TitleViewSet(ModelViewSet):
    """ViewSet для работы с произведениями."""
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    http_method_names = [
        'get', 'post', 'patch', 'delete', 'head', 'options', 'trace'
    ]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitleSerializer
        return CreateTitleSerializer

    def get_queryset(self):
        return (
            Title.objects.annotate(rating=Avg('reviews__score'))
            .order_by('-year')
        )


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


class ReviewViewSet(CommmentReviewMixin):
    """ViewSet для работы с отзывами."""
    serializer_class = ReviewSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['title'] = get_object_or_404(
            Title, pk=self.kwargs.get('title_id')
        )
        return context

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(CommmentReviewMixin):
    """ViewSet для работы с комментариями."""
    serializer_class = CommentSerializer

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all().order_by('pub_date')

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )
