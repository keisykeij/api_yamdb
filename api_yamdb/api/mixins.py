from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.viewsets import GenericViewSet
from rest_framework.filters import SearchFilter

from .permissions import IsAdminOrReadOnly


class BaseMixinSet(CreateModelMixin, ListModelMixin,
                   DestroyModelMixin, GenericViewSet):
    """
    Класс, объединяющий различные миксины для создания, получения списка и удаления моделей.
    """
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
