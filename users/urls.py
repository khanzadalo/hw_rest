from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/users/registration/', views.RegistrationAPIView.as_view()),
    path('api/v1/users/confirm/', views.ConfirmUserAPIView.as_view()),
    path('api/v1/users/login/', views.LoginAPIView.as_view()),
    path('api/v1/users/logout/', views.LogoutAPIView.as_view()),


]