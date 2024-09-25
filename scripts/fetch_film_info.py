import os
import requests.exceptions
from dotenv import load_dotenv
import tmdbsimple as tmdb
from datetime import datetime
from imdb import Cinemagoer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MovieRater.settings')
import django

django.setup()
from main.models import Genre, Movie, Collection, Ratings

load_dotenv()
tmdb.API_KEY = os.getenv('TMDB_API_KEY')


def get_imdb_rating(imdb_id):
    ia = Cinemagoer()
    imdb_movie = ia.get_movie(imdb_id.replace('tt', ''))
    rating = imdb_movie.get('rating')
    votes = imdb_movie.get('votes')
    return rating, votes


def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None


def get_latest_index():
    with open('i.txt', 'r', encoding='utf-8') as file:
        index = file.read()
    return index


def save_latest_index(i):
    with open('i.txt', 'w', encoding='utf-8') as file:
        file.write(i)


i = int(get_latest_index())
print("starting_id: ", i)
while True:
    try:
        movie = tmdb.Movies(i)
        response = movie.info()

        title = movie.title
        overview = movie.overview
        release_date = parse_date(movie.release_date)
        runtime = movie.runtime
        budget = movie.budget
        revenue = movie.revenue
        poster_path = movie.poster_path
        poster_url = f"https://image.tmdb.org/t/p/original{poster_path}" if poster_path else ''
        backdrop_path = movie.backdrop_path
        backdrop_url = f"https://image.tmdb.org/t/p/original{backdrop_path}" if backdrop_path else ''
        tagline = movie.tagline
        adult = movie.adult
        imdb_id = movie.imdb_id
        original_title = movie.original_title

        if imdb_id:
            imdb_rating, imdb_vote_count = get_imdb_rating(imdb_id)
        else:
            imdb_rating, imdb_vote_count = None, None

        belongs_to_collection = movie.belongs_to_collection
        collection_obj = None
        if belongs_to_collection:
            collection_data = belongs_to_collection
            collection_obj, _ = Collection.objects.get_or_create(
                name=collection_data['name'],
                defaults={
                    'poster_path': collection_data['poster_path'],
                    'backdrop_path': collection_data['backdrop_path']
                }
            )

        movie_obj, created = Movie.objects.get_or_create(
            title=title,
            defaults={
                'overview': overview,
                'release_date': release_date,
                'runtime': runtime,
                'revenue': revenue,
                'budget': budget,
                'poster_url': poster_url,
                'backdrop_url': backdrop_url,
                'tagline': tagline,
                'adult': adult,
                'imdb_id': imdb_id,
                'original_title': original_title,
                'belongs_to_collection': collection_obj,
            }
        )

        if not created:
            movie_obj.overview = overview
            movie_obj.release_date = release_date
            movie_obj.runtime = runtime
            movie_obj.revenue = revenue
            movie_obj.budget = budget
            movie_obj.poster_url = poster_url
            movie_obj.backdrop_url = backdrop_url
            movie_obj.tagline = tagline
            movie_obj.adult = adult
            movie_obj.imdb_id = imdb_id
            movie_obj.original_title = original_title
            movie_obj.belongs_to_collection = collection_obj
            movie_obj.save()

        Ratings.objects.update_or_create(
            movie=movie_obj,
            defaults={
                'tmdb_popularity': movie.popularity,
                'tmdb_vote_average': movie.vote_average,
                'tmdb_vote_count': movie.vote_count,
                'imdb_rating': imdb_rating,
                'imdb_vote_count': imdb_vote_count,
            }
        )

        genres_array = movie.genres
        genres = []
        for genre in genres_array:
            genre_name = genre['name']
            if genre_name:
                genres.append(genre_name)
                genre_obj, _ = Genre.objects.get_or_create(name=genre_name)
                movie_obj.genres.add(genre_obj)

        print(f"ID: {i}   Movie '{title}' ")
        i += 1
    except requests.exceptions.HTTPError:
        i += 1
        pass
    except KeyboardInterrupt:
        print("Terminated at id: ", i)
        save_latest_index(str(i))
        break
    except Exception as e:
        print(f"Terminated at id: {i} due to error: {e}")
        save_latest_index(str(i))
        i += 1
        continue
