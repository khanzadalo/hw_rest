from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import serializer, models
from rest_framework import status


@api_view(['GET', 'POST'])
def movie_list_view(request):
    if request.method == 'GET':
        movie = models.Movie.objects.all()
        data = serializer.MovieSerializer(movie, many=True).data
        return Response(data)
    elif request.method == 'POST':
        movie = models.Movie.objects.create(**request.data)
        return Response(data=serializer.MovieSerializer(movie).data,
                        status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail_view(request, id):
    try:
        movie_id = models.Movie.objects.get(id=id)
    except models.Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={"message": "Movie not found"})

    if request.method == 'GET':
        data = serializer.MovieSerializer(movie_id).data
        return Response(data=data)
    elif request.method == 'DELETE':
        movie_id.delete()
        return Response(status=status.HTTP_204_NO_CONTENT,
                        data={"message": "Movie has been deleted"})
    elif request.method == 'PUT':
        movie_id.name = request.data.get('title')
        movie_id.description = request.data.get('description')
        movie_id.duration = request.data.get('duration')
        movie_id.director = request.data.get('director')
        movie_id.save()
        return Response(data=serializer.MovieSerializer(movie_id).data)


@api_view(['GET', 'POST'])
def directors_list_view(request):
    if request.method == 'GET':
        director = models.Director.objects.all()
        data = serializer.DirectorSerializer(director, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        director = models.Director.objects.create(**request.data)
        return Response(data=serializer.DirectorSerializer(director).data,
                        status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def director_detail_view(request, id):
    try:
        director_id = models.Director.objects.get(id=id)
    except models.Director.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'message': 'Director not found'})

    if request.method == 'GET':
        data = serializer.DirectorSerializer(director_id).data
        return Response(data=data)
    elif request.method == 'DELETE':
        director_id.delete()
        return Response(status=status.HTTP_204_NO_CONTENT,
                        data={"message": "Director has been deleted"})
    elif request.method == 'PUT':
        director_id.name = request.data.get('name')
        director_id.save()
        return Response(data=serializer.DirectorSerializer(director_id).data)


@api_view(['GET', 'POST'])
def review_list_view(request):
    if request.method == 'GET':
        review = models.Review.objects.all()
        data = serializer.ReviewSerializer(review, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        review = models.Review.objects.create(**request.data)
        return Response(data=serializer.ReviewSerializer(review).data,
                        status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_view(request, id):
    try:
        review_id = models.Review.objects.get(id=id)
    except models.Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={"message": "Review does not exist"})

    if request.method == 'GET':
        data = serializer.ReviewSerializer(review_id).data
        return Response(data=data)
    elif request.method == 'DELETE':
        review_id.delete()
        return Response(status=status.HTTP_204_NO_CONTENT,
                        data={"message": "Review has been deleted"})
    elif request.method == 'PUT':
        review_id.text = request.data.get('text')
        review_id.movie = request.data.get('movie')
        review_id.stars = request.data.get('stars')
        review_id.save()
        return Response(data=serializer.ReviewSerializer(review_id).data)


@api_view(['GET'])
def movies_reviews_view(request):
    movie_reviews = models.Movie.objects.all()
    data = serializer.MovieSerializer(movie_reviews, many=True).data
    return Response(data=data)



