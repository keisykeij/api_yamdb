from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from reviews.models import Title
from .permissions import IsAuthorOrReadOnly
from .serializers import (ReviewSerializer, )


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )
