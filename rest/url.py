from django.urls import path, include
from rest import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("api", views.getRoutes),

    # pyJWT
    path("api/registration_api2", views.Registration_api_2.as_view(), name="registration_api2"),
    path("api/login_api2", views.Login_api_2.as_view(), name="login_api2"),

    # simpleJWT
    path("api/registration_api", views.Registration_api.as_view(), name="registration_api"),
    path("api/login_api", views.Login_api.as_view(), name="login_api"),
    path("api/logout_api", views.Logout_api.as_view(), name="logout_api"),

    path('api/token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

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
