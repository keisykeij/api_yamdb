from django.core.mail import send_mail


def send_confirmation_code(confirmation_code: str, recipient_mail: str):
    send_mail(
        subject='Подтверждение регистрации',
        message=(
            'Благодарим Вас за регистрацию на нашем сервисе!\n'
            'Для прохождения аутентификации Вам необходимо '
            'предоставить код подтверждения:\n'
            f'Ваш код: {confirmation_code}.'
        ),
        from_email='yamdb@yandex.ru',
        recipient_list=[recipient_mail,],
        fail_silently=True
    )
