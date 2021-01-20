import random
from django.shortcuts import render

def index(request):
    return render(request, "index.html")


def bus(request):
    return render(request, "bus.html")


def vue(request):
    return render(request, "vue.html")


def movies(request):
    return render(request, "movies.html")


def chart(request):
    labels = ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"]
    data = [12, 19, 3, 5, 2, 3]
    context = {"labels": labels, "data": data}

    return render(request, 'chart.html', context)
    
def logout(request):
    return render(request, "index.html") # TODO

def synthesis(request):
    return render(request, "synthesis.html")

def obligations(request):
    return render(request, "obligations.html")

def skills(request):
    return render(request, "skills.html")

def courses(request):
    return render(request, "courses.html")
