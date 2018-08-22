from django.urls import path

from shop import views

urlpatterns = [
    path('', views.home, name="home"),
    path('product/<slug>', views.details, name="product"),
    path('review/<slug>/post', views.review, name="review"),
    path('signup/', views.signup, name="signup"),
    path('login/', views.mylogin, name="login"),
    path('logout/', views.mylogout, name="logout"),
]