from . import models
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class MovieSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField()
    director = serializers.SerializerMethodField()

    class Meta:
        model = models.Movie
        fields = 'id title description duration director reviews count_reviews all_reviews rating'.split()

    def get_director(self, movie):
        try:
            return f'{movie.director.name} - {movie.director.id}'
        except AttributeError:
            return "Director does not exist"

    def get_reviews(self, movie):
        serializer = ReviewSerializer(models.Review.objects.filter(author__isnull=False,
                                                                   movie=movie), many=True)
        return serializer.data


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


class ReviewCreateSerializer(serializers.Serializer):
    stars = serializers.IntegerField(min_value=1, max_value=5)
    text = serializers.CharField(max_length=60)


class MovieValidateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=3, max_length=100)
    description = serializers.CharField(required=False, default='')
    duration = serializers.IntegerField(min_value=0.5, max_value=1000000)
    director_id = serializers.IntegerField(allow_null=True, required=False,
                                           default=None)
    reviews = serializers.ListField(child=ReviewCreateSerializer())

    def validate_director_id(self, director_id):

        if models.Director.objects.filter(id=director_id).count() == 0:
            raise ValidationError(f"Director with id {director_id} does not exist")
        return director_id


class DirectorValidateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=2, max_length=100)


class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField()
    stars = serializers.IntegerField()
    movie = serializers.CharField()