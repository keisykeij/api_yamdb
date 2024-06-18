from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from .models import Title
from .serializers import TitleSerializer


class TitleViewSet(ModelViewSet):
    """ViewSet для работы с произведениями."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


