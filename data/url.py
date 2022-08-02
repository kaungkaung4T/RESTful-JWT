from django.urls import path
from data import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("registration", views.registration, name="registration"),
    path("logout", views.logout, name="logout"),
    path("update_item/<str:pk>", views.update_item, name="update_item"),
    path("delete_item/<str:pk>", views.delete_item, name="delete_item"),
]
