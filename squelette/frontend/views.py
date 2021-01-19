import random
from django.shortcuts import render


menu = {"menu": [
    {"name": "Index", "class": "fas fa-home", "url": "front_index"},
    {"name": "Bus", "class": "fas fa-bus", "url": "front_bus"},
    {"name": "Vue", "class": "fas fa-eye", "url": "front_vue"},
    {"name": "Movies", "class": "fas fa-star", "url": "front_movies"}
]}


def index(request):
    return render(request, "index.html", menu)


def bus(request):
    return render(request, "bus.html", menu)


def vue(request):
    return render(request, "vue.html", menu)




def movies(request):
    return render(request, "movies.html", menu)
