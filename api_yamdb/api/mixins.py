from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.viewsets import GenericViewSet


class BaseMixinSet(CreateModelMixin, ListModelMixin,
                   DestroyModelMixin, GenericViewSet):
    """
    Класс, объединяющий различные миксины для создания, получения списка и удаления моделей.
    """
    pass
