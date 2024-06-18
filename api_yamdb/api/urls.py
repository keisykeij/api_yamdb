from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TitleViewSet

router = DefaultRouter()
router.register(r'titles', TitleViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]
