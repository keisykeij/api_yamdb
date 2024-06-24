from django.db.models import Avg
from django.shortcuts import get_object_or_404

from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend

from .mixins import BaseMixinSet
from .permissions import IsAdminOrReadOnly, IsAuthorModeratorAdminOrReadOnly
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

    def get_queryset(self):
        return Category.objects.all()


class GenreViewSet(BaseMixinSet):
    """ViewSet для работы с жанрами."""
    serializer_class = GenreSerializer

    def get_queryset(self):
        return Genre.objects.all()


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    http_method_names = [
        'get', 'post', 'patch', 'delete', 'head', 'options', 'trace'
    ]

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


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    http_method_names = [
        'get', 'post', 'patch', 'delete', 'head', 'options', 'trace'
    ]

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all().order_by('pub_date')

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )
