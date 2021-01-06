import random

from django.http import HttpResponse
from django.shortcuts import render

from backend.models import Cat, Kibble

def index(request):
    # names = ("Miaous", "Garfield", "Grosminet", "O'Malley", "Tom")

    # for name in names:
    # 	cat = Cat(name=name, age=random.randint(1,18), weight=random.randint(2,10))
    # 	cat.save()

    context = {}
    context["cats"] = Cat.objects.all()
    print(Cat.objects.all())
    return render(request, "animals.html", context)

def about(request):
    return HttpResponse("About")