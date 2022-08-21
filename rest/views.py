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

        # Creating tokens and refresh with pyjwt
        "/api/registration_api2",
    ]

    return Response(routes)


            #  *** -------------
            #
            # token create session
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
                payload = {
                    "id": user.id,
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                    "iat": datetime.datetime.utcnow()
                }

                key = "secret"
                token = jwt.encode(payload, key, algorithm="HS256")

                response = Response()
                response.set_cookie(key='jwt', value=token, httponly=True)
                response.data = {
                    "jwt": token
                }
                return response







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
