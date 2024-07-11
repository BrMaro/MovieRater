from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from main.models import Movie, Ratings, Genre, Collection
import pprint


# Create your views here.

def index(request):
    return HttpResponse("Hello, World!")


def home(request):
    return render(request, "main/home.html")


def movie_page(response, movie_id):
    movie = get_object_or_404(Movie, movie_id=movie_id)
    if movie:
        movie_ratings = get_object_or_404(Ratings, movie=movie)
        movie_genres = movie.genres.all()
        movie_collection = movie.belongs_to_collection

        movie_data = {
            'title': movie.title,
            'overview': movie.overview,
            'release_date': movie.release_date,
            'runtime': movie.runtime,
            'adult':movie.adult,
            'poster_url': movie.poster_url,
            'backdrop_url': movie.backdrop_url,
            'tagline': movie.tagline,
            'original_title': movie.original_title,
            'tmdb_popularity': movie_ratings.tmdb_popularity,
            'tmdb_vote_average': movie_ratings.tmdb_vote_average,
            'imdb_rating': movie_ratings.imdb_rating,
            'imdb_vote_count': movie_ratings.imdb_vote_count,
            'genres': movie_genres
        }
        if movie_collection:
            movie_data['collection_name'] = movie_collection['name'],
            movie_data['collection_poster_path'] = movie_collection['poster_path'],
            movie_data['collection_backdrop_path'] = movie_collection['backdrop_path']

        pprint.pprint(movie_data)
        return render(response, 'main/movie_page.html', movie_data)


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
