import json
import urllib.request

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from .models import *


# Create your views here.


def index(request):
    return HttpResponse("Hello, world. This is PASS !")


def get_etudiant(request):
    id = request.user.pk
    if request.user.is_authenticated:
        response = Etudiant.objects.get(pk=id)
        response = serializers.serialize('json', [response,])
    else:
        response = ''
    return JsonResponse(response, safe=False)


