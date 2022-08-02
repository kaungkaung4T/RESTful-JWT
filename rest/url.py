from django.urls import path, include
from rest import views

urlpatterns = [
    path("api", views.getRoutes),

    # POSTMAN
    path("resting", views.Resting.as_view(), name="resting"),
    path("resting/<str:pk>", views.Resting.as_view(), name="update"),
    path("resting/<str:pk>", views.Resting.as_view(), name="delete"),

    # Default
    path("rest", views.get, name="get"),
    path("rest/post", views.post, name="post"),
    path("rest/put/<str:pk>", views.put, name="put"),
    path("rest/delete/<str:pk>", views.delete, name="delete"),

    path("api-auth", include("rest_framework.urls"))
]
