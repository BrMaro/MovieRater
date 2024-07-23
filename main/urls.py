from django.urls import path
from . import views

urlpatterns = [
    path("index/", views.index, name="index"),
    path("", views.home2, name="home2"),
    path("api/movies/", views.movies_json, name="movies_json"),
    path('movie/<int:movie_id>', views.movie_page, name="movie_page"),
    path('collections/', views.collections, name='collections'),
    path('collections/<int:collection_id>', views.collection_page, name='collection_page'),
    path('table_display', views.table_display, name='table_display')
]
