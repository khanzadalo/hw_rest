import random
from django.core.mail import send_mail
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from Afisha import settings
from .models import UserConfirmation
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserConfirmationSerializer


class RegistrationAPIView(APIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(**serializer.validated_data)

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

        return Response(data={'message': 'User created successfully'},
                        status=status.HTTP_201_CREATED)


class ConfirmUserAPIView(APIView):
    serializer_class = UserConfirmationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
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


class LoginAPIView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.validated_data)
        if user:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            user.save()
            return Response({'token': token.key})
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response({'message': 'User logged out'}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({'message': 'User is already logged out'}, status=status.HTTP_200_OK)

