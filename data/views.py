from django.shortcuts import render
from data.form import ItemForm
# Create your views here.


def index(request):
    i = ItemForm()
    return render(request, "index.html", {"i":i})


def registration(request):
    return render(request, "registration.html")


def login(request):
    return render(request, "login.html")
