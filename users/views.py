from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from movie_app import models, serializer
from users.serializers import UserValidateSerializer, UserLoginSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated


@api_view(['POST'])
def registration_view(request):
    if request.method == 'POST':
        serializer = UserValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        User.objects.create_user(**serializer.validated_data)
        return Response(data={'message': 'User created successfully'},
                        status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.validated_data)
        if user:
            Token.objects.filter(user=user).delete()
            # try:
            #     token = Token.objects.get(user=user)
            # except Token.DoesNotExist:

            token = Token.objects.create(user=user)
            return Response(data={'key': token.key}, status=status.HTTP_200_OK)

        return Response(data={'error': 'User not Found'},
                        status=status.HTTP_404_NOT_FOUND)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def user_reviews(request):
    reviews = models.Review.objects.filter(author=request.user)
    serializers = serializer.ReviewSerializer(reviews, many=True)
    return Response(data=serializers.data)
