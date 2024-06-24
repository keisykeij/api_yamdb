from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from .serializers import (AdminUserSerializer, UserRegisterSerializer,
                          UserSerializer, UserTokenSerializer)
from .utils import send_confirmation_code

from api.permissions import IsAppAdmin

User = get_user_model()


class UserCreateAPIView(CreateAPIView):
    """Регистрация пользователя через username и email."""

    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.status_code = status.HTTP_200_OK

        current_user = get_object_or_404(User, **response.data)

        confirmation_code = default_token_generator.make_token(
            user=current_user
        )

        send_confirmation_code(confirmation_code, current_user.email)

        return response


class UserTokenView(APIView):
    """Предоставление токена зарегистрированному пользователю."""

    permission_classes = (AllowAny,)

    def post(self, request: Request):
        serializer = UserTokenSerializer(
            data=request.data
        )
        if serializer.is_valid():
            try:
                user = get_object_or_404(
                    User,
                    username=serializer.validated_data.get('username', None)
                )
            except Http404:
                raise NotFound('Пользователь не найден.')
            token_status = default_token_generator.check_token(
                user=user, token=serializer.validated_data['confirmation_code']
            )

            if not token_status:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            token = AccessToken.for_user(user=user)
            return Response(
                {'token': str(token)},
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class UserViewSet(ModelViewSet):
    """
    ViewSet для администрирования пользователями, а также для
    получения и редактирования профиля пользователем.
    """

    serializer_class = AdminUserSerializer
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    permission_classes = (IsAppAdmin,)
    pagination_class = PageNumberPagination

    http_method_names = [
        'get', 'post', 'patch', 'delete', 'head', 'options', 'trace'
    ]

    def get_queryset(self):
        return User.objects.all()

    @action(
        detail=False,
        methods=('get', 'patch'),
        url_path='me',
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request: Request):
        user = get_object_or_404(User, id=request.user.id)

        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data)

            if serializer.is_valid():
                user = serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
