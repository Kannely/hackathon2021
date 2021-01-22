import random
from django.shortcuts import render

def index(request):
    return render(request, "index.html")

import urllib.request

from django.conf import settings

import urllib.request
from urllib.error import HTTPError

def __get_sso_url__(request, suffix):
    if settings.SSO_URL:
        return settings.SSO_URL + suffix
    else:
        return request.build_absolute_uri(settings.SSO_PREFIX + suffix)

def login(request):
    return render(request, "login.html", { "login_url": __get_sso_url__(request, "login") })
    
def __do_logout__(request):
    cookie = request.headers.get("Cookie")
    url = __get_sso_url__(request, "logout")
    new_request = urllib.request.Request(url)
    if cookie:
        new_request.add_header("Cookie", cookie)
    try:
        response = urllib.request.urlopen(new_request)
    except:
        pass

def logout(request):
    __do_logout__(request)
    return render(request, "logout.html")

def synthesis(request):
    return render(request, "synthesis.html")

def obligations(request):
    return render(request, "obligations.html")

def skills(request):
    return render(request, "skills.html")

def courses(request):
    return render(request, "courses.html")
