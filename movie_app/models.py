from django.db import models
from django.contrib.auth.models import User


class Director(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    duration = models.IntegerField()
    director = models.ForeignKey('Director', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

    @property
    def count_reviews(self):
        return self.reviews.all().count()

    @property
    def all_reviews(self):
        reviews = Review.objects.filter(movie=self)
        return [{'id': i.id, 'text': i.text, 'stars': i.stars} for i in reviews]

    @property
    def rating(self):
        reviews_count = self.reviews.count()
        sum = self.reviews.aggregate(sum('stars'))['stars__sum']
        try:
            return round(sum / reviews_count, 1)
        except:
            return 0


class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, related_name='reviews')
    stars = models.PositiveSmallIntegerField(choices=[(1, '⭐'), (2, '⭐⭐'), (3, '⭐⭐⭐'), (4, '⭐⭐⭐⭐'), (5, '⭐⭐⭐⭐⭐')],
                                             default=1)

    def __str__(self):
        return self.text
