from django.urls import path

from .views import UserRegisterView, UserTokenView

app_name = 'users'

API_V1 = 'v1'

urlpatterns = [
    path(
        f'{API_V1}/auth/signup/',
        UserRegisterView.as_view(),
        name='user_signup'
    ),
    path(
        f'{API_V1}/auth/token/',
        UserTokenView.as_view(),
        name='user_token'
    ),
]
