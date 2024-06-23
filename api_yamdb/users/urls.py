from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserCreateAPIView, UserTokenView, UserViewSet

app_name = 'users'

API_V1 = 'v1'

router_v1 = DefaultRouter()

router_v1.register('users', UserViewSet, basename='users_admin')

urlpatterns = [
    path(
        f'{API_V1}/auth/signup/',
        UserCreateAPIView.as_view(),
        name='user_signup'
    ),
    path(
        f'{API_V1}/auth/token/',
        UserTokenView.as_view(),
        name='user_token'
    ),
    path(f'{API_V1}/', include(router_v1.urls)),
]
