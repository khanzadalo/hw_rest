from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.views import APIView

from .models import Review
from . import serializers, models
from .serializers import ReviewSerializer


class MovieListApiView(ListCreateAPIView):
    queryset = models.Movie.objects.all()
    serializer_class = serializers.MovieSerializer
    pagination_class = PageNumberPagination
    filterset_fields = ['title']

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MovieDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = models.Movie.objects.all()
    serializer_class = serializers.MovieSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class DirectorsListApiView(ListCreateAPIView):
    queryset = models.Director.objects.all()
    serializer_class = serializers.DirectorSerializer
    pagination_class = PageNumberPagination
    filterset_fields = ['name']

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DirectorDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = models.Director.objects.all()
    serializer_class = serializers.DirectorSerializer
    lookup_field = 'id'


    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class ReviewListApiView(ListCreateAPIView):
    queryset = models.Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    filterset_fields = ['text', 'movie']

    def post(self, request, *args, **kwargs):
        user = request.user
        if not user.email_confirmed:
            return Response('Email not confirmed', status=status.HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReviewDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = serializers.ReviewValidateSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class MoviesReviewsApiView(APIView):
    def get(self, request, *args, **kwargs):
        movie_reviews = models.Movie.objects.all()
        data = serializers.MovieSerializer(movie_reviews, many=True).data
        return Response(data)



