from django.urls import include, path
from rest_framework import routers

from .views import ReviewViewSet, CommentViewSet


API_V1 = 'v1'

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review')
router_v1.register(
    r'titles/(?P<title_id>\d+)/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comment')

urlpatterns = [
    path(f'{API_V1}/', include(router_v1.urls)),
]
