from django.shortcuts import render
from data.models import Item
from rest.serializer import ItemSerializer
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.

# CBV Tested with POST man
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

    def put(self, pk, request):
        item = Item.objects.get(id=pk)
        its = ItemSerializer(item, data=request.data)
        if its.is_valid():
            its.save()
            return Response(its.data)
        return Response(its.errors)

    def delete(self, pk):
        item = Item.objects.get(id=pk)
        item.delete()
        data = {"success": "success"}
        return Response(data=data)

