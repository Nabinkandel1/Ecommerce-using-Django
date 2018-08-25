from django.urls import path

from shop import views
app_name = "shop"

urlpatterns = [
    path('', views.home, name="home"),
    path('product/<slug>', views.details, name="detail"),
    path('review/<slug>/post', views.review, name="review"),
    path('signup/', views.signup, name="signup"),
    path('login/', views.mylogin, name="login"),
    path('logout/', views.mylogout, name="logout"),
    path('search/', views.product_search, name="search"),
    path('search_api/', views.product_search_api, name="search_api"),
    path('add_to_cart/', views.add_to_cart, name="add_to_cart"),
    path('my_cart/', views.my_cart, name="my_cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('category/<slug>/', views.categories, name="category"),
]
