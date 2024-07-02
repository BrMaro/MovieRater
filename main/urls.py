from django.urls import path
from . import views

urlpatterns = [
    path("index/", views.index, name = "index"),
    path("", views.home, name="home"),
    path("api/movies/", views.movies_json, name="movies_json")
]