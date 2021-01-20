import json
from django.http import HttpResponse, JsonResponse

import urllib.request
from urllib.error import HTTPError

PASS_PREFIX = "/pass/"


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. This is the back-end !")


def __get_pass_url__(request, suffix):
    return request.build_absolute_uri(PASS_PREFIX + suffix)


def __make_json_request__(request, url, transfer_cookie=True, array=True, fields_only=False):
    cookie = request.headers.get("Cookie")
    new_request = urllib.request.Request(url)
    if transfer_cookie and cookie:
        new_request.add_header("Cookie", cookie)
    try:
        url = urllib.request.urlopen(new_request)
        data = json.loads(url.read().decode())
        if fields_only:
            if array:
                data = data[1:-1]['fields']
            else:
                data = data[0]['fields']
        return data, 200
    except HTTPError as err:
        return {}, err.code


def get_synthesis(request):
    url = __get_pass_url__(request, 'etudiant')
    etudiant_data, etudiant_code = __make_json_request__(request, url, fields_only=True)
    return JsonResponse(etudiant_data, status=etudiant_code)
