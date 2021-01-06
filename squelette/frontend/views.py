import random

from django.http import HttpResponse
from django.shortcuts import render

from backend.models import Cat, Kibble

    
menu = {"menu": [
    { "name": "Index", "class": "fas fa-cat", "url": "front_index" },
    { "name": "About", "class": "fas fa-dog", "url": "front_about" }
]}

def index(request):
    return render(request, "index.html", menu)

def about(request):
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

