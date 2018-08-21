from django.urls import path

from shop import views

urlpatterns = [
    path('', views.home),
    path('product/<slug>', views.details),
    path('review/<slug>/post', views.review),
    path('signup/', views.signup),
    path('login/', views.login),
]