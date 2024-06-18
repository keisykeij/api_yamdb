from rest_framework.viewsets import ModelViewSet


from .serializers import TitleSerializer
from reviews.models import Title


class TitleViewSet(ModelViewSet):
    """ViewSet для работы с произведениями."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


