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
        return Response(data=data)
    elif request.method == 'POST':
        serializers = serializer.MovieCreateUpdateSerializer(data=request.data)
        if not serializers.is_valid():
            return Response(data={'errors': serializers.errors},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        print(request.data)
        title = request.data.get("title")
        description = request.data.get("description")
        duration = request.data.get("duration")
        director_id = request.data.get("director_id")

        movie = models.Movie.objects.create(title=title, description=description, duration=duration,
                                            director_id=director_id)
        for i in request.data.get("reviews", []):
            models.Review.objects.create(stars=i['stars'], text=i['text'], movie=movie)

        # movie = models.Movie.objects.create(**request.data)

        return Response(data=serializer.MovieSerializer(movie).data,
                        status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail_view(request, id):
    try:
        movie = models.Movie.objects.get(id=id)
    except models.Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={"message": "Movie not found"})

    if request.method == 'GET':
        data = serializer.MovieSerializer(movie).data
        return Response(data=data)
    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT,
                        data={"message": "Movie has been deleted"})
    elif request.method == 'PUT':
        movie.title = request.data.get('title')
        movie.description = request.data.get('description')
        movie.duration = request.data.get('duration')
        movie.director_id = request.data.get('director_id')
        movie.save()
        return Response(data=serializer.MovieSerializer(movie).data)


@api_view(['GET', 'POST'])
def directors_list_view(request):
    if request.method == 'GET':
        director = models.Director.objects.all()
        data = serializer.DirectorSerializer(director, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        serializers = serializer.DirectorValidateSerializer(data=request.data)

        if not serializers.is_valid():
            return Response(data={'errors': serializers.errors},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        name = request.data.get('name')
        director = models.Director.objects.create(**request.data)
        director.save()
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
        serializers = serializer.DirectorValidateSerializer(data=request.data)
        if serializers.is_valid():
            return Response(data={'errors': serializers.errors},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
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
        serializers = serializer.ReviewValidateSerializer(data=request.data)
        if not serializers.is_valid():
            return Response(data={'errors': serializers.errors},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        text = request.data.get('text')
        movie = request.data.get('movie')
        stars = request.data.get('stars')
        review = models.Review.objects.create(text=text, movie=movie,
                                              stars=stars)
        review.save()
        return Response(data=serializer.ReviewSerializer(review).data,
                        status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_view(request, id):
    try:
        review = models.Review.objects.get(id=id)
    except models.Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={"message": "Review does not exist"})

    if request.method == 'GET':
        data = serializer.ReviewSerializer(review).data
        return Response(data=data)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT,
                        data={"message": "Review has been deleted"})
    elif request.method == 'PUT':
        serializers = serializer.ReviewValidateSerializer(data=request.data)
        if not serializers.is_valid():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data={'errors': serializers.errors})
        review.text = request.data.get('text')
        review.movie = request.data.get('movie')
        review.stars = request.data.get('stars')
        review.save()
        return Response(data=serializer.ReviewSerializer(review).data)


@api_view(['GET'])
def movies_reviews_view(request):
    movie_reviews = models.Movie.objects.all()
    data = serializer.MovieSerializer(movie_reviews, many=True).data
    return Response(data=data)



