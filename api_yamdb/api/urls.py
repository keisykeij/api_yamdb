from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet, GenreViewSet, TitleViewSet, ReviewViewSet
)

API_V1 = 'v1'

app_name = 'api'

router = DefaultRouter()
router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(r'category', CategoryViewSet, basename='categories')
router_v1.register(r'genre', GenreViewSet, basename='genres')

router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)

urlpatterns = [
    path(f'{API_V1}/', include(router_v1.urls)),
