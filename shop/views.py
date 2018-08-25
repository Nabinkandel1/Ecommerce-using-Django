from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

from shop.forms import SignUpForm, ReviewForm
from shop.models import Category, Product, Review
from shop.serializers import ProductSerializer


def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    carts = Product.objects.filter(slug__in=request.session.get('items', []))
    data = {
        "categories": categories,
        "products": products,
        "carts": carts,
            }
    return render(request, "shop/index.html", data)


def details(request, slug):
    product = get_object_or_404(Product, slug=slug)
    categories = Category.objects.all()
    reviewform = ReviewForm()
    carts = Product.objects.filter(slug__in=request.session.get('items', []))
    data = {
        "product": product,
        "reviewform": reviewform,
        "carts": carts,
        "categories": categories
    }
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
            user.is_active = True
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
def product_search(request):
    if request.method == 'GET':
        query = request.GET.get("q", "")
        products = Product.objects.filter(Q(title__contains=query) | Q(description__contains=query))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def add_to_cart(request):
    if request.method == 'POST':
        slug = request.POST.get("slug", "")
        product = get_object_or_404(Product, slug=slug)
        items = request.session.get('items', [])
        if slug not in items:
            amount = request.session.get('cart_amount', 0.0)
            items.append(product.slug)
            request.session['items'] = items
            request.session['cart_amount'] = amount + float(product.price)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


@api_view(['GET'])
def my_cart(request):
    if request.method == 'GET':
        products = Product.objects.filter(slug__in=request.session.get('items', []))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


def checkout(request):
    request.session['items'] = []
    request.session['cart_amount'] = 0
    return redirect("shop:home")


@api_view(['GET'])
def categories(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)