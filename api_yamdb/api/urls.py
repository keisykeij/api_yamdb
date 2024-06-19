from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, GenreViewSet, TitleViewSet

router = DefaultRouter()
router.register(r'titles', TitleViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'genre', GenreViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]
