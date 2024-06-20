from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import serializers

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Пользователь не может иметь такой username.'
            )
        return value

    def validate(self, attrs):
        try:
            object_for_username = get_object_or_404(
                User, username=attrs.get('username')
            )
        except Http404:
            object_for_username = None
        try:
            object_for_email = get_object_or_404(
                User, email=attrs.get('email')
            )
        except Http404:
            object_for_email = None

        if object_for_email != object_for_username:
            raise serializers.ValidationError(
                'Неправильные учетные данные.'
            )

        return attrs


class UserTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')

    def validate_confirmation_code(self, value):
        status = default_token_generator.check_token(
            user=self.instance, token=value
        )

        if not status:
            raise serializers.ValidationError(
                'Неверный код подтверждения'
            )

        return value
