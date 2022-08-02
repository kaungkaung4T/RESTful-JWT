from django.urls import path, include
from rest import views

urlpatterns = [
    path("rest", views.Resting.as_view(), name="resting"),
    path("api-auth", include("rest_framework.urls"))
]
