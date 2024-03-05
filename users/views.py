import random

from django.core.mail import send_mail
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from Afisha import settings
from .models import UserConfirmation
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserConfirmationSerializer


@api_view(['POST'])
def registration_api_view(request):
    if request.method == 'POST':
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Генерируем и сохраняем код подтверждения в базе данных
        code = ''.join([str(random.randint(0, 9)) for _ in range(5)])
        confirmation = UserConfirmation.objects.create(user=user, code=code)
        confirmation.save()

        # Отправляем код подтверждения на почту
        subject = 'Код для подтверждения'
        message = f'Ваш код подтверждения: {code}'
        sender = settings.EMAIL_HOST_USER
        recipient_list = [user.email]
        send_mail(subject, message, sender, recipient_list)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def confirm_user_api_view(request):
    serializer = UserConfirmationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    code = serializer.validated_data.get('code')

    # Проверяем, существует ли код подтверждения в базе данных
    try:
        confirmation = UserConfirmation.objects.get(code=code)
    except UserConfirmation.DoesNotExist:
        return Response({'error': 'Invalid confirmation code'}, status=status.HTTP_404_NOT_FOUND)

    # Активируем пользователя, если код совпадает
    user = confirmation.user
    user.is_active = True
    user.save()
    confirmation.delete()  # Удаляем код подтверждения после использования

    return Response({'status': 'User activated'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def login_api_view(request):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = authenticate(**serializer.validated_data)
    if user:
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        user.save()
        return Response({'token': token.key})
    return Response({'error': 'Invalid credentials'}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({'message': 'User logged out'}, status=status.HTTP_200_OK)
    except Token.DoesNotExist:
        return Response({'message': 'User is already logged out'}, status=status.HTTP_200_OK)

