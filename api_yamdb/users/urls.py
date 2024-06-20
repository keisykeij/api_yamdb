from django.urls import path

from .views import UserRegisterView, UserTokenView

app_name = 'users'

urlpatterns = [
    path(
        'signup/', UserRegisterView.as_view(), name='user_signup'
    ),
    path('token/', UserTokenView.as_view(), name='user_token'),
]
