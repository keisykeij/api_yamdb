from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import serializers

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователей."""

    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=(UnicodeUsernameValidator(),)
    )

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

    def save(self, **kwargs):
        self.instance, status = User.objects.get_or_create(
            **self.validated_data
        )
        return self.instance


class UserTokenSerializer(serializers.ModelSerializer):
    """Сериализатор для выдачи токена зарегистрированному пользователю."""

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class AdminUserSerializer(serializers.ModelSerializer):
    """Сериализатор для администрирования пользователей администратором."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class UserSerializer(AdminUserSerializer):
    """Сериализатор для получения и частичного обновления профиля."""
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': False}
        }
