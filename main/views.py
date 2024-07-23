from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from main.models import Movie, Ratings, Genre, Collection
import pprint
import random

tmdb_image_link = 'https://image.tmdb.org/t/p/w500'


def format_runtime(minutes):
    hours, minutes = divmod(minutes, 60)
    if hours > 0:
        return f"{hours}h {minutes} min"
    else:
        return f"{minutes} min"


def format_number(number):
    return "{:,}".format(number)


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
            'adult': movie.adult,
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
            movie_data['collection_name'] = str(movie_collection.name).replace("('", '').replace("',)", "")
            movie_data['collection_poster_path'] = movie_collection.poster_path
            movie_data['collection_backdrop_path'] = movie_collection.backdrop_path
            movie_data['other_movies_in_collection'] = Movie.objects.filter(
                belongs_to_collection=movie_collection).exclude(movie_id=movie_id)

        return render(response, 'main/movie_page.html', movie_data)


def movies_json(request):
    movies = Movie.objects.all().values('movie_id', 'title', 'overview', 'poster_url', 'backdrop_url', 'tagline')
    movies_list = []
    for movie in movies:
        movie_id = movie['movie_id']
        movie_ratings = get_object_or_404(Ratings, movie_id=movie_id)
        movie_data = {
            'movie_id': movie['movie_id'],
            'title': movie['title'],
            'overview': movie['overview'],
            'poster_url': movie['poster_url'],
            'tmdb_popularity': movie_ratings.tmdb_popularity,
            'backdrop_url': movie['backdrop_url'],
            'tagline': movie['tagline']
        }
        movies_list.append(movie_data)
    return JsonResponse(movies_list, safe=False)


def collections(response):
    collections_list = Collection.objects.all().values('collection_id', 'name', 'poster_path', 'backdrop_path')

    collections_data = []
    for collection in collections_list:
        collection_id = collection['collection_id']
        movies_in_collection = Movie.objects.filter(belongs_to_collection=collection_id)
        collection_data = {
            'collection_id': collection_id,
            'name': collection['name'],
            'poster_path': tmdb_image_link + str(collection['poster_path']),
            'movies_in_collection': movies_in_collection,
        }
        collections_data.append(collection_data)
    pprint.pprint(collections_data[0])
    return render(response, 'main/collections.html', {'collections': collections_data})


def collection_page(response, collection_id):
    collection = get_object_or_404(Collection, collection_id=collection_id)

    movies_in_collection = Movie.objects.filter(belongs_to_collection=collection_id)
    collection_data = {
        'collection_id': collection_id,
        'collection_name': collection.name,
        'collection_poster_path': tmdb_image_link + str(collection.poster_path),
        'collection_backdrop_path': tmdb_image_link + str(collection.backdrop_path),
        'movies_in_collection': movies_in_collection,
    }

    return render(response, 'main/collection_page.html', collection_data)


def table_display(response):
    movies = Movie.objects.all()
    movielist_data = []
    for movie in movies:
        movie_ratings = get_object_or_404(Ratings, movie=movie)
        movie_genres = movie.genres.all()
        movie_collection = movie.belongs_to_collection

        movie_data = {
            'title': movie.title,
            'overview': movie.overview,
            'release_date': movie.release_date,
            'runtime': format_runtime(movie.runtime),
            'adult': movie.adult,
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
            movie_data['collection_name'] = str(movie_collection.name).replace("('", '').replace("',)", "")
            movie_data['collection_poster_path'] = movie_collection.poster_path
            movie_data['collection_backdrop_path'] = movie_collection.backdrop_path
            movie_data['num_of_movies_in_collection'] = len(
                Movie.objects.filter(belongs_to_collection=movie_collection))

        movielist_data.append(movie_data)

    sorted_movielist_data = sorted(movielist_data, key=lambda x: x['tmdb_popularity'], reverse=True)

    return render(response, 'main/table_display.html', {'movies': sorted_movielist_data})


def home2(request):
    movies = Movie.objects.all()
    movielist_data = []
    for movie in movies:
        movie_ratings = get_object_or_404(Ratings, movie=movie)
        movie_genres = movie.genres.all()
        movie_collection = movie.belongs_to_collection

        movie_data = {
            'movie_id': movie.movie_id,
            'title': movie.title,
            'overview': movie.overview,
            'release_date': movie.release_date,
            'runtime': format_runtime(movie.runtime),
            'adult': movie.adult,
            'poster_url': movie.poster_url,
            'backdrop_url': movie.backdrop_url,
            'tagline': movie.tagline,
            'original_title': movie.original_title,
            'tmdb_popularity': movie_ratings.tmdb_popularity if movie_ratings.tmdb_popularity is not None else 0,            'tmdb_vote_count':movie_ratings.tmdb_vote_count if movie_ratings.tmdb_vote_count is not None else 0,
            'tmdb_vote_average': movie_ratings.tmdb_vote_average if movie_ratings.tmdb_vote_average is not None else 0,
            'imdb_rating': movie_ratings.imdb_rating if movie_ratings.imdb_rating is not None else 0,
            'imdb_vote_count': movie_ratings.imdb_vote_count if movie_ratings.imdb_rating is not None else 0,
            'genres': movie_genres
        }

        if movie_collection:
            movie_data['collection_name'] = str(movie_collection.name).replace("('", '').replace("',)", "")
            movie_data['collection_poster_path'] = movie_collection.poster_path
            movie_data['collection_backdrop_path'] = movie_collection.backdrop_path
            movie_data['num_of_movies_in_collection'] = len(
                Movie.objects.filter(belongs_to_collection=movie_collection))

        movielist_data.append(movie_data)

    movielist_data = [i for i in movielist_data if (i['tmdb_vote_count']+i['imdb_vote_count'])>=10000]

    tmdb_top = sorted(movielist_data, key=lambda x: x['tmdb_vote_average'], reverse=True)[:20]
    imdb_top = sorted(movielist_data, key=lambda x: x['imdb_rating'], reverse=True)[:20]
    tmdb_trending = sorted(movielist_data, key=lambda x: x['tmdb_popularity'], reverse=True)[:20]
    random.shuffle(movielist_data)
    
    context = {
        'tmdb_top': tmdb_top,
        'imdb_top': imdb_top,
        'tmdb_trending': tmdb_trending,
        'random_order': movielist_data[:20]
    }

    return render(request, "main/home2.html", context)
