from rest_framework import serializers
from . import models


class DirectorSerializer(serializers.ModelSerializer):
    movies_count = serializers.SerializerMethodField()

    class Meta:
        model = models.Director
        fields = 'id name movies_count'.split()

    def get_movies_count(self, movie):
        return models.Movie.objects.filter(director=movie).count()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField()
    director = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = models.Movie
        fields = 'id title duration director reviews count_reviews all_reviews rating'.split()


    def get_director(self, movie):
        try:
            return movie.director.name
        except AttributeError:
            return "No Director"

    def get_reviews(self, movie):
        serializer = ReviewSerializer(models.Review.objects.filter(author__isnull=False,
                                                                   movie=movie), many=True)
        return serializer.data

    def get_rating(self, obj):
        reviews = models.Review.objects.filter(movie=obj)
        return sum(review.stars for review in reviews) / reviews.count() if reviews else 0


