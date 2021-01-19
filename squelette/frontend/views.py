import random
from django.shortcuts import render

from backend.models import Cat, Kibble

menu = {"menu": [
    {"name": "Connexion", "url": "front_login", "logged": False},
    {"name": "Ma fiche", "url": "front_synthesis", "logged": True},    
    {"name": "Conditions de diplomation", "url": "front_obligations", "logged": True},
    {"name": "Compétences", "url": "front_skills", "logged": True},
    {"name": "UEs", "url": "front_courses", "logged": True},
    {"name": "Déconnexion", "url": "front_logout", "logged": True},
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


def chart(request):
    labels = ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"]
    data = [12, 19, 3, 5, 2, 3]

    context = menu
    context["labels"] = labels
    context["data"] = data

    return render(request, 'chart.html', context)

def login(request):
    return render(request, "index.html", menu) # TODO
    
def logout(request):
    return render(request, "index.html", menu) # TODO

def synthesis(request):
    return render(request, "synthesis.html", menu)

def obligations(request):
    return render(request, "obligations.html", menu)

def skills(request):
    return render(request, "skills.html", menu)

def courses(request):
    return render(request, "courses.html", menu)
