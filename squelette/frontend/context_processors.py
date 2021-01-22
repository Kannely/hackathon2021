def add_menu_to_context(request):
    return {"menu": [
    {"name": "Connexion", "url": "front_login", "class": "fas fa-user-circle", "logged": False},
    {"name": "Ma fiche", "url": "front_synthesis", "class": "fas fa-sticky-note", "logged": True},    
    {"name": "Conditions de diplomation", "url": "front_obligations", "class": "fas fa-flag-checkered", "logged": True},
    {"name": "Compétences", "url": "front_skills", "class": "fas fa-check-double", "logged": True},
    {"name": "UEs", "url": "front_courses", "class": "fas fa-book-open", "logged": True},
    {"name": "Déconnexion", "url": "front_logout", "class": "fas fa-user-circle", "logged": True},
]}


import json
import urllib.request

from django.conf import settings

import urllib.request
from urllib.error import HTTPError

def __get_sso_url__(request, suffix):
    if settings.SSO_URL:
        return settings.SSO_URL + suffix
    else:
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
        return data
    except HTTPError as err:
        return None

def add_authentification_status_to_context(request):
    return {"is_authenticated": True if __get_user__(request) else False}
