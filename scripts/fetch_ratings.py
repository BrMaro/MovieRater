import os
from dotenv import load_dotenv
import requests
import tmdbsimple as tmdb
import json

load_dotenv()

tmdb.API_KEY = os.getenv('TMDB_API_KEY')
for i in range(300,301):
    try:
        movie = tmdb.Movies(i)
        response = movie.info()
        print(response)
        print(json.dumps(response,indent=4))
        # print(f"{i} Movie Title: {movie.title}--------------------------- Budget: {'{:,}'.format(movie.budget)}")
    except:
        pass
