import json
import urllib.request

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from .models import *

import urllib.request
from urllib.error import HTTPError

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. This is PASS !")

def __get_sso_url__(request, suffix):
    return request.build_absolute_uri(settings.SSO_PREFIX + suffix)
    
def __get_user__(request):
    cookie = request.headers.get("Cookie")
    url = __get_sso_url__(request, "user")
    new_request = urllib.request.Request(url)
    if cookie:
        new_request.add_header("Cookie", cookie)
    try:
        response = urllib.request.urlopen(new_request)
        data = json.loads(response.read().decode())
        return data[0]
    except HTTPError as err:
        return None


def __get_etudiant_from_request__(request):
    user = __get_user__(request)
    if user:
        _id = user['pk']
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


def get_ue(request, id):
    obj = UE.objects.filter(pk=id).first()
    return __get_json_or_404__(obj, array=False)


def get_competence(request, id):
    obj = Competence.objects.filter(pk=id).first()
    return __get_json_or_404__(obj, array=False)


def get_periode(request, id):
    obj = Periode.objects.filter(pk=id).first()
    return __get_json_or_404__(obj, array=False)


def get_taf(request, id):
    obj = TAF.objects.filter(pk=id).first()
    return __get_json_or_404__(obj, array=False)


def get_ue_suivi(request, id):
    obj = SuivreUE.objects.filter(pk=id).first()
    return __get_json_or_404__(obj, array=False)


def get_eval_competence(request, id):
    obj = EvalCompetence.objects.filter(pk=id).first()
    return __get_json_or_404__(obj, array=False)


def get_formation(request, id):
    obj = Formation.objects.filter(pk=id).first()
    return __get_json_or_404__(obj, array=False)


def get_obligation(request, id):
    obj = Obligations.objects.filter(pk=id).first()
    return __get_json_or_404__(obj, array=False)


def get_all_ue(request):
    objs = UE.objects.all()
    return __get_json_or_404__(objs)


def get_all_competence(request):
    objs = Competence.objects.all()
    return __get_json_or_404__(objs)
