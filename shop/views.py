from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

# Create your views here.
from shop import urls
from shop.forms import SignUpForm
from shop.models import Category, Product, Review


def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    data = {
        "categories": categories,
        "products": products
            }
    return render(request, "shop/index.html", data)


def details(request, slug):
    return render(request, "shop/details.html")


def review(request, slug):
    pass


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('shop:login')
    else:
        form = SignUpForm()
        return render(request, "shop/signup.html", {"form": form})


def mylogin(request):
    if request.user.is_authenticated:
        return redirect("shop:home")
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            if user.is_active:
                return redirect("shop:home")
    return render(request, "shop/login.html")


def mylogout(request):
    logout(request)
    return redirect("shop:home")