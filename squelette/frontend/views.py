import random, json
import urllib.request

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from backend.models import Cat, Kibble

menu = {"menu": [
    { "name": "Index", "class": "fas fa-cat", "url": "front_index" },
    { "name": "About", "class": "fas fa-dog", "url": "front_about" },
    { "name": "Animals", "class": "fas fa-heart", "url": "front_animals" },
    { "name": "Vue", "class": "fas fa-fish", "url": "front_vue" },
    { "name": "Movies", "class": "fas fa-paw", "url": "front_movies" }
]}

def index(request):
    return render(request, "index.html", menu)

def about(request):
    return render(request, "about.html", menu)

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
	name = "Bruce"
	surname = "Willis"
	result_url = "http://127.0.0.1:8000/back/actor/{}/{}/".format(name, surname)
	with urllib.request.urlopen(result_url) as url:
		data = json.loads(url.read().decode())
	context = {}
	context["movies"] = data
	print(context["movies"])
	return render(request, "movies.html", context)