from django.shortcuts import render, redirect
from data.models import Item
from data.form import ItemForm
from django.contrib.auth.models import User, auth
from django.contrib import messages
# Create your views here.


def index(request):
    item = Item.objects.all()
    itemForm = ItemForm()
    return render(request, "index.html",
                  {"item": item, "itemForm":itemForm})


def registration(request):
    if request.method == "POST":
        user = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 == password2:
            if User.objects.filter(username=user).exists():
                messages.info(request, "Username already exist")
                return redirect("registration")

            if User.objects.filter(email=email).exists():
                messages.info(request, "Email already exist")
                return redirect("registration")

            User.objects.create_user(username=user, email=email, password=password1)
            messages.success(request, "Account created")
            return redirect("login")

        else:
            messages.info(request, "Passwords are not same")
            return redirect("registration")


    return render(request, "registration.html")


def login(request):
    if request.method == "POST":
        user = request.POST["username"]
        password1 = request.POST["password1"]

        u = auth.authenticate(username=user, password=password1)

        if u:
            auth.login(request, u)
            return redirect("/")

        messages.info(request, "Couldn't find your account")
        return redirect("login")

    return render(request, "login.html")


def logout(request):
    auth.logout(request)
    return redirect("login")
