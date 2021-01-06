import random

from django.http import HttpResponse
from django.shortcuts import render

from backend.models import Cat, Kibble

def index(request):
    names = ("Miaous", "Garfield", "Grosminet", "O'Malley", "Tom")

    cats = []
    for name in names:
        cats.append({
            "name": name,
            "age": random.randint(1,18),
            "weight": random.randint(2,10),
        })

    context = {}
    context["cats"] = Cat.objects.all()
    Cat.objects.filter(name="Zorro").delete()
    cat = Cat(name='Zorro', age=16, weight=4)
    cat.save()
    print(Cat.objects.all())
    return render(request, "index.html", context)

def about(request):
    return HttpResponse("About")