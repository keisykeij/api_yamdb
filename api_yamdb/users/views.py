from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .serializers import UserRegisterSerializer, UserTokenSerializer
from .utils import send_confirmation_code

User = get_user_model()


class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
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

            send_confirmation_code(confirmation_code, current_user.email)

            return Response(
                serializer.data, status=status.HTTP_200_OK
            )
        # TODO: отправка сообщения пользователю с кодом подтверждения
            # send_mail()
            # return Response(
            #     {'confirmation_code': confirmation_code},
            #     status=status.HTTP_200_OK
            # )

        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class UserTokenView(APIView):
    permission_classes = [AllowAny]

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
