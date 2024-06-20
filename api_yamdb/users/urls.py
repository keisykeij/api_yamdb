from django.urls import path

from .views import UserRegisterView, UserTokenView

app_name = 'users'

urlpatterns = [
    path(
        'v1/auth/signup/', UserRegisterView.as_view(), name='user_signup'
    ),
    path('v1/auth/token/', UserTokenView.as_view(), name='user_token'),
]
