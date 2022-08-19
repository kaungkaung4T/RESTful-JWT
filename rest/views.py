from django.shortcuts import render
from django.contrib.auth.models import auth
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
    ]

    return Response(routes)

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

                return Response(data={
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })

        error = {
            "error":"error",
        }
        return Response(data=error)


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
