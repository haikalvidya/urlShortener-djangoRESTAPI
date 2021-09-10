from django.urls import path
from shorter import views

urlpatterns = [
    path('', views.home, name="Home"),
    path('shorten', views.shorter_url, name="ShortUrl"),
    path('<str:hash_id>/', views.redirector, name="Redirector"),
]
