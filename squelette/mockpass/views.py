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
            return HttpResponse(response, content_type='application/json')
    else:
        if obj:
            response = serializers.serialize('json', [obj])
            return HttpResponse(response, content_type='application/json')
    return JsonResponse({}, status=404)


def get_etudiant(request):
    etudiant = __get_etudiant_from_request__(request)
    return __get_json_or_404__(etudiant, array=False)


def get_ue(request, _id):
    obj = UE.objects.filter(pk=_id).first()
    return __get_json_or_404__(obj, array=False)


def get_competence(request, _id):
    obj = Competence.objects.filter(pk=_id).first()
    return __get_json_or_404__(obj, array=False)


def get_periode(request, _id):
    obj = Periode.objects.filter(pk=_id).first()
    return __get_json_or_404__(obj, array=False)


def get_taf(request, _id):
    obj = TAF.objects.filter(pk=_id).first()
    return __get_json_or_404__(obj, array=False)


def get_ue_suivi(request, _id):
    obj = SuivreUE.objects.filter(pk=_id).first()
    return __get_json_or_404__(obj, array=False)


def get_eval_competence(request, _id):
    obj = EvalCompetence.objects.filter(pk=_id).first()
    return __get_json_or_404__(obj, array=False)


def get_formation(request, _id):
    obj = Formation.objects.filter(pk=_id).first()
    return __get_json_or_404__(obj, array=False)


def get_obligation(request, _id):
    obj = Obligations.objects.filter(pk=_id).first()
    return __get_json_or_404__(obj, array=False)
