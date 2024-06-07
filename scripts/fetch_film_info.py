import os
import requests.exceptions
from dotenv import load_dotenv
import tmdbsimple as tmdb
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MovieRater.settings')
import django

django.setup()
from main.models import Genre, Movie, Collection

load_dotenv()

tmdb.API_KEY = os.getenv('TMDB_API_KEY')


def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None


for i in range(1, 100):
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
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else ''
        tagline = movie.tagline

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
                'tagline': tagline,
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
            movie_obj.tagline = tagline
            movie_obj.belongs_to_collection = collection_obj
            movie_obj.save()

        genres_array = movie.genres
        genres = []
        for genre in genres_array:
            genre_name = genre['name']
            if genre_name:
                genres.append(genre_name)
                genre_obj, _ = Genre.objects.get_or_create(name=genre_name)
                movie_obj.genres.add(genre_obj)

        print(
            f"ID: {i}   Movie '{title}' added  Genres: {', '.join(genres)},  Collection: {collection_obj}, and poster URL: {poster_url}")
    except requests.exceptions.HTTPError:
        pass
