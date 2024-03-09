from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.RegistrationAPIView.as_view()),
    path('confirm/', views.ConfirmUserAPIView.as_view()),
    path('login/', views.LoginAPIView.as_view()),
    path('logout/', views.LogoutAPIView.as_view()),


]