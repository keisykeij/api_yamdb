from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin, ListModelMixin
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.filters import SearchFilter

from .permissions import (
    IsAuthorOrModeratorOrAdminOrReadOnly, IsAdminOrReadOnly
)


class BaseMixinSet(CreateModelMixin, ListModelMixin,
                   DestroyModelMixin, GenericViewSet):
    """
    Класс, объединяющий различные миксины для создания,
    получения списка и удаления моделей.
    """
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CommmentReviewMixin(ModelViewSet):
    """
    Класс, объединяющий различные миксины для создания, редактирования,
    получения списка и удаления моделей Comment и Review.
    """
    permission_classes = (IsAuthorOrModeratorOrAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    http_method_names = [
        'get', 'post', 'patch', 'delete', 'head', 'options', 'trace'
    ]
