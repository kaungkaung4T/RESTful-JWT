from django.urls import path
from data import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("registration", views.registration, name="registration"),
]
