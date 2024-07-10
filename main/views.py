from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from main.models import Movie, Ratings
import pprint


# Create your views here.

def index(request):
    return HttpResponse("Hello, World!")


def home(request):
    return render(request, "main/home.html")


def movies_json(request):
    movies = Movie.objects.all().values('movie_id', 'title', 'overview', 'poster_url', 'backdrop_url', 'tagline')
    movies_list = []
    for movie in movies:
        movie_id = movie['movie_id']
        movie_ratings = get_object_or_404(Ratings, movie_id=movie_id)
        movie_data = {
            'title': movie['title'],
            'overview': movie['overview'],
            'poster_url': movie['poster_url'],
            'tmdb_popularity': movie_ratings.tmdb_popularity,
            'backdrop_url': movie['backdrop_url'],
            'tagline': movie['tagline']
        }
        movies_list.append(movie_data)
    return JsonResponse(movies_list, safe=False)
