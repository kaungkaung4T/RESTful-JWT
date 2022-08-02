from django.shortcuts import render
from data.form import ItemForm
# Create your views here.


def index(request):
    i = ItemForm()
    return render(request, "index.html", {"i":i})
