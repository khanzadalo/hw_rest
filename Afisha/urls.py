from movie_app import views
from django.contrib import admin
from django.urls import path
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/movies/', views.movie_list_view),
    path('api/v1/movies/<int:id>/', views.movie_detail_view),
    path('api/v1/directors/', views.directors_list_view),
    path('api/v1/directors/<int:id>/', views.director_detail_view),
    path('api/v1/reviews/', views.review_list_view),
    path('api/v1/reviews/<int:id>/', views.review_detail_view),
    path('api/v1/movies/reviews/', views.movies_reviews_view),
    path('api/v1/register/', user_views.registration_view),
    path('api/v1/login/', user_views.login_view),
    path('api/v1/user/reviews', user_views.user_reviews),
]
