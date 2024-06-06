from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(response):
    return HttpResponse("Hello, WOrld!")

def home(response):
    return render(response,"main/base.html")