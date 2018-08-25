from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

from shop.forms import SignUpForm, ReviewForm
from shop.models import Category, Product, Review
from shop.serializers import ProductSerializer


def get_payload(request, title=""):
    return {
        "title": title,
        "categories": Category.objects.filter(active=True),
        "carts": Product.objects.filter(slug__in=request.session.get('items', []))
    }


def home(request):
    data = get_payload(request, "Home")
    data["products"] = Product.objects.filter(active=True)
    return render(request, "shop/index.html", data)


def details(request, slug):
    product = get_object_or_404(Product, slug=slug)
    data = get_payload(request, product.title)
    data["product"] = product
    data["reviewform"] = ReviewForm()
    return render(request, "shop/details.html", data)


def review(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.user.is_authenticated and request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
        return redirect('shop:detail', product.slug)
    else:
        form = SignUpForm()
        return render(request, "shop/signup.html", {"form": form})


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


@api_view(['GET'])
def product_search_api(request):
    query = request.GET.get("q", "")
    products = Product.objects.filter(Q(title__contains=query) | Q(description__contains=query))
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


def product_search(request):
    query = request.GET.get("q", "")
    data = get_payload(request, query + " - search result")
    data["products"] = Product.objects.filter(Q(title__contains=query) | Q(description__contains=query))
    return render(request, 'shop/products.html', data)


def my_cart(request):
    data = get_payload(request, "My cart")
    data["products"] = Product.objects.filter(slug__in=request.session.get('items', []))
    return render(request, 'shop/products.html', data)


def checkout(request):
    request.session['items'] = []
    request.session['cart_amount'] = 0
    return redirect("shop:home")


def categories(request, slug):
    category = get_object_or_404(Category, slug=slug)
    data = get_payload(request, category.title)
    data["products"] = Product.objects.filter(category=category)
    return render(request, "shop/products.html", data)


def add_to_cart(request):
    if request.method == 'POST':
        slug = request.POST.get("slug", "")
        product = Product.objects.filter(slug=slug).first()
        if product:
            items = request.session.get('items', [])
            if slug not in items:
                items.append(product.slug)
                amount = request.session.get('cart_amount', 0.0) + float(product.price)
                request.session['items'] = items
                request.session['cart_amount'] = amount
                return JsonResponse({"status": "ok", "message": product.title + " added to cart",
                                     "count": len(items), "amount": amount})
            return JsonResponse({"status": "fail", "message": "Item already added"})
        return JsonResponse({"status": "fail", "message": "Item not found"})
    return JsonResponse({"status": "fail", "message": "Only post method allowed"})

