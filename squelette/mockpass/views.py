import json
import urllib.request

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from .models import *
from django.shortcuts import get_object_or_404


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. This is PASS !")


def get_etudiant(request):
    id = request.user.pk
    response = HttpResponse(status=404)
    if request.user.is_authenticated:
        response = get_object_or_404(Etudiant, user=id)
        response = serializers.serialize('json', [response,])
        response = JsonResponse(response, safe=False)
    return response


