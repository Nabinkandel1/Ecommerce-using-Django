from django.shortcuts import render

# Create your views here.
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
    return render(request, "shop/signup.html")


def login(request):
    return render(request, "shop/login.html")