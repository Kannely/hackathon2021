import json
import urllib.request

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from .models import *


# Create your views here.

def index(request):
    return HttpResponse("Hello, world. This is PASS !")

def __get_etudiant_from_request__(request):
    _id = request.user.pk
    if request.user.is_authenticated:
        etudiant = Etudiant.objects.filter(user.pk==_id)
        if etudiant:
            return etudiant
    return None

def get_etudiant(request):
    etudiant = __get_etudiant_from_request__(request)
    if etudiant:
        response = 
        return JsonResponse()
