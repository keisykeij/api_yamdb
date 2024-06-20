from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import AllowAny

from .serializers import UserRegisterSerializer, UserTokenSerializer

User = get_user_model()


class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                current_user = get_object_or_404(
                    User,
                    username=serializer.validated_data['username'],
                    email=serializer.validated_data['email']
                )
            except Http404:
                current_user = serializer.save()

            confirmation_code = default_token_generator.make_token(
                user=current_user
            )

            return Response(
                {'confirmation_code': confirmation_code},
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class UserTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request):
        try:
            user = get_object_or_404(
                User, username=request.data.get('username', None)
            )
            serializer = UserTokenSerializer(
                user, data=request.data, context={'request': request}
            )
            if serializer.is_valid():
                token = AccessToken.for_user(user=user)
                return Response(
                    {'token': str(token)},
                    status=status.HTTP_200_OK
                )
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        except Http404:
            raise NotFound('Пользователь не найден.')
