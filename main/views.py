from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from main.models import Movie

# Create your views here.

def index(response):
    return HttpResponse("Hello, WOrld!")


def home(response):
    return render(response, "main/base.html")


def movies_json(response):
    movies = Movie.objects.all().values('title', 'overview', 'poster_url')
    print(movies)
    movies_list = list(movies)
    # print(movies_list[:3])
    return JsonResponse(movies_list, safe=False)
