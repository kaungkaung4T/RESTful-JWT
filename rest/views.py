from django.shortcuts import render
from data.models import Item
from rest.serializer import ItemSerializer
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse

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
        "/api/token",
        "/api/token/refresh",
        "api/registration",
        "api/login",
    ]

    return Response(routes)








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
