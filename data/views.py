from django.shortcuts import render, redirect
from data.models import Item
from data.form import ItemForm
from django.contrib.auth.models import User, auth
from django.contrib import messages
# Create your views here.


def index(request):
    if request.method == "POST":
        if User.objects.filter(username=request.user).exists():
            itemForm = ItemForm(request.POST, request.FILES)
            if itemForm.is_valid():
                instance = itemForm.save(commit=False)
                instance.user = request.user
                instance.save()
                messages.success(request, "Uploaded Item")
                return redirect("/")

        messages.info(request, "Please login to upload item")
        return redirect("/")

    item = Item.objects.all()
    itemForm = ItemForm()
    return render(request, "index.html",
                  {"item": item, "itemForm":itemForm})


def update_item(request, pk):
    item = Item.objects.get(id=pk)
    if request.method == "POST":
        if User.objects.filter(username=request.user).exists():
            itemForm = ItemForm(request.POST, request.FILES, instance=item)
            if itemForm.is_valid():
                instance = itemForm.save(commit=False)
                instance.user = request.user
                instance.save()
                messages.success(request, "Updated Item")
                return redirect("/")

        messages.info(request, "Please login to update item", extra_tags="info")
        return redirect("/")

    itemForm = ItemForm(instance=item)
    return render(request, "update_item.html",
                  {"itemForm":itemForm})


def delete_item(request, pk):
    if request.method == "POST":
        if User.objects.filter(username=request.user).exists():
            item = Item.objects.get(id=pk)
            item.delete()
            messages.success(request, "Deleted Item")
            return redirect("/")

        messages.info(request, "Please login")
        return redirect("/")


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




