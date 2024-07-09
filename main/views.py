from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from main.models import Movie, Ratings
import pprint

# Create your views here.

def index(request):
    return HttpResponse("Hello, World!")


def home(request):
    return render(request, "main/base.html")


def movies_json(request):
    movies = Movie.objects.all().values('movie_id', 'title', 'overview', 'poster_url')
    movies_list = []
    for movie in movies:
        movie_id = movie['movie_id']
        movie_ratings = get_object_or_404(Ratings, movie_id=movie_id)
        movie_data = {
            'title': movie['title'],
            'overview': movie['overview'],
            'poster_url': movie['poster_url'],
            'tmdb_popularity': movie_ratings.tmdb_popularity
        }
        movies_list.append(movie_data)
    pprint.pprint(movies_list)
    return JsonResponse(movies_list, safe=False)
