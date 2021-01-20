import json
import urllib.request

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from .models import *


# Create your views here.

def index(request):
    return HttpResponse("Hello, world. This is PASS !")


def __get_etudiant_from_request__(request):
    if request.user.is_authenticated:
        _id = request.user.pk
        etudiant = Etudiant.objects.filter(user=_id).first()
        if etudiant:
            return etudiant
    return None


def __get_json_or_404__(obj, array=True):
    if array:
        if obj and len(obj) > 0 and obj[0]:
            response = serializers.serialize('json', obj)
            return JsonResponse(response, safe=False)
    else:
        if obj:
            response = serializers.serialize('json', [obj])
            return JsonResponse(response, safe=False)
    return JsonResponse({}, status=404)


def get_etudiant(request):
    etudiant = __get_etudiant_from_request__(request)
    return __get_json_or_404__(etudiant, array=False)


def get_ue(request, id):
    pass


def get_competence(request, id):
    pass


def get_periode(request, id):
    pass


def get_taf(request, id):
    pass


def get_ue_suivi(request, id):
    pass


def get_eval_competence(request, id):
    pass


def get_formation(request, id):
    pass


def get_obligation(request, id):
    pass
