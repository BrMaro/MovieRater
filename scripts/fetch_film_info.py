import os
import requests.exceptions
from dotenv import load_dotenv
import tmdbsimple as tmdb
from datetime import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MovieRater.settings')
import django
django.setup()
from main.models import Genre, Movie

load_dotenv()

tmdb.API_KEY = os.getenv('TMDB_API_KEY')

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None


for i in range(8088,10000):
    try:
        movie = tmdb.Movies(i)
        response = movie.info()

        title = movie.title
        overview = movie.overview
        release_date = parse_date(movie.release_date)
        runtime = movie.runtime
        budget = movie.budget
        revenue = movie.revenue

        movie_obj, created = Movie.objects.get_or_create(
            title=title,
            defaults = {
                'overview': overview,
                'release_date': release_date,
                'runtime': runtime,
                'revenue': revenue,
                'budget': budget,
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

        print(f"ID: {i}   Movie '{title}' added to the database with genres: {', '.join(genres)}")
    except requests.exceptions.HTTPError:
        pass
