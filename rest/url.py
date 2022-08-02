from django.urls import path, include
from rest import views

urlpatterns = [
    path("rest", views.Resting.as_view(), name="resting"),
    path("rest/<str:pk>", views.Resting.as_view(), name="update"),
    path("rest/<str:pk>", views.Resting.as_view(), name="delete"),
    path("api-auth", include("rest_framework.urls"))
]
