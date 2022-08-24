import datetime
import jwt
from django.shortcuts import render
from django.contrib.auth.models import auth, User
from data.models import Item
from rest.serializer import ItemSerializer
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from rest.serializer import UserSerializer
from rest.serializer import LoginSerializer

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest.authentication import access_encode, access_decode, refresh_encode, refresh_decode
# Create your views here.


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(["GET"])
def getRoutes(request):
    routes = [
        # Creating tokens and refresh with SIMPLE JWT
        "/api/token",
        "/api/token/refresh",

        # Creating tokens and refresh MANUALLY with SIMPLE JWT
        "/api/registration_api",
        "/api/login_api",
        "/api/logout_api",

        # Creating tokens and refresh with pyjwt
        "/api/registration_api2",
        "/api/loin_api2",
        "/api/refresh_api2",
        "/api/user_api2",
        "/api/logout_api2",
    ]

    return Response(routes)







            #  *** -------------
            #
            # token create session with pyjwt
            #
            #  ------------- ***





# Creating tokens with pyjwt
class Registration_api_2(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        us = UserSerializer(data=request.data)
        if us.is_valid():
            us.save()
            return Response(us.data)
        return Response(us.errors)


class Login_api_2(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        ls = LoginSerializer(data=request.data)
        if ls.is_valid():
            user = auth.authenticate(username=ls.data["username"], password=ls.data["password"])

            if user:
                user = User.objects.get(username=ls.data["username"])
                access = access_encode(user)
                refresh = refresh_encode(user)

                response = Response()
                response.set_cookie(key="refresh_token", value=refresh, httponly=True)

                response.data = {
                    "access": access,
                    "refresh": refresh,
                }
                return response

from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
class User_api2(APIView):
    def get(self, request):
        auth = get_authorization_header(request).split()

        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            id = access_decode(token)

            user = User.objects.filter(pk=id).first()
            us = UserSerializer(user)
            return Response(us.data)

        raise AuthenticationFailed('unauthenticated')


class Refresh_api2(APIView):
    def post(self, request):
        token = request.COOKIES.get("refresh_token")

        response = Response()
        id = refresh_decode(token)

        user = User.objects.get(id=id)
        access = access_encode(user)

        response.data = {
            "access":access,
        }
        return response


class Logout_api2(APIView):
    def post(self, _):
        response = Response()
        response.delete_cookie(key="refresh_token")
        response.data = {
            "success": "success",
        }
        return response







            # *** -------------
            #
            # token create session MANUALLY with SIMPLE JWT
            #
            #  ------------- ***





# Creating tokens MANUALLY with SIMPLE JWT
class Registration_api(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        us = UserSerializer(data=request.data)
        if us.is_valid():
            us.save()
            return Response(us.data)
        return Response(us.errors)


class Login_api(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        ls = LoginSerializer(data=request.data)
        if ls.is_valid():
            user = auth.authenticate(username=ls.data["username"], password=ls.data["password"])

            if user:
                refresh = RefreshToken.for_user(user)
                # response = Response()
                # response.set_cookie(key='refresh_token', value=refresh, httponly=True)

                data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                return Response(data=data, status=status.HTTP_201_CREATED)

        error = {
            "error":"error",
        }
        return Response(data=error)


# NO need to do this, JUST A TEST
class User_api(APIView):
    def post(self, request):
        token = request.data.get("refresh_token")
        payload = jwt.decode(token, "django-insecure-by-sfr1)qov@nvb$8cni97k5i%^hr_x93-r@66ee^v=2$uavwl", algorithms="HS256")
        user = User.objects.get(id=payload["user_id"])
        us = UserSerializer(user)
        return Response(us.data)


class Logout_api(APIView):

    def post(self, request, format=None):
        try:
            token = request.data.get('refresh_token')
            token_obj = RefreshToken(token)
            token_obj.blacklist()

            return Response(status=status.HTTP_200_OK)

        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)








            #  *** -------------
            #
            # model api create session
            #
            #  ------------- ***





# CBV Tested with POST man, all tests have been successed
class Resting(APIView):
    # authentication_classes = (
    #     JwtAuthentication, BearerAuthenticationAllowInactiveUser, SessionAuthenticationAllowInactiveUser
    # )
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        item = Item.objects.all()
        its = ItemSerializer(item, many=True)
        return Response(its.data)

    def post(self, request):
        item = ItemSerializer(data=request.data)
        if item.is_valid():
            item.save()
            return Response(item.data)
        return Response(item.errors)

    def put(self, request, pk):
        item = Item.objects.get(id=pk)
        its = ItemSerializer(item, data=request.data)
        if its.is_valid():
            its.save()
            return Response(its.data)
        return Response(its.errors)

    def delete(self, request, pk):
        item = Item.objects.get(id=pk)
        item.delete()
        data = {"success": "success"}
        return Response(data=data)


# FBV default, all tests have been successed
@api_view(["GET"])
def get(request):
    item = Item.objects.all()
    its = ItemSerializer(item, many=True)
    return Response(its.data)


@api_view(["POST"])
def post(request):
    its = ItemSerializer(data=request.data)
    if its.is_valid():
        its.save()
        return Response(its.data)
    return Response(its.errors)


@api_view(["PUT"])
def put(request, pk):
    item = Item.objects.get(id=pk)
    its = ItemSerializer(item, data=request.data)
    if its.is_valid():
        its.save()
        return Response(its.data)
    return Response(its.errors)


@api_view(["DELETE"])
def delete(request, pk):
    item = Item.objects.get(id=pk)
    item.delete()
    data = {"success":"success"}
    return Response(data=data)
