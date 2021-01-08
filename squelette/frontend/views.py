import random
from django.shortcuts import render

from backend.models import Cat, Kibble

menu = {"menu": [
    {"name": "Index", "class": "fas fa-home", "url": "front_index"},
    {"name": "Bus", "class": "fas fa-bus", "url": "front_bus"},
    {"name": "Animals", "class": "fas fa-cat", "url": "front_animals"},
    {"name": "Vue", "class": "fas fa-eye", "url": "front_vue"},
    {"name": "Movies", "class": "fas fa-star", "url": "front_movies"}
]}


def index(request):
    return render(request, "index.html", menu)


def bus(request):
    return render(request, "bus.html", menu)


def vue(request):
    return render(request, "vue.html", menu)


def animals(request):
    # names = ("Marie", "Berlioz", "Toulouse", "Pistache")

    # for name in names:
    # 	cat = Cat(name=name, age=random.randint(1,18), weight=random.randint(2,10))
    # 	cat.save()
    context = menu
    context["cats"] = Cat.objects.all()
    print(Cat.objects.all())
    return render(request, "animals.html", context)


def movies(request):
    return render(request, "movies.html", menu)
