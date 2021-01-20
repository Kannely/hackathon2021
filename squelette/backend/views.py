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


def __make_json_request__(request, url, transfer_cookie=True, fields_only=False):
    cookie = request.headers.get("Cookie")
    new_request = urllib.request.Request(url)
    if transfer_cookie and cookie:
        new_request.add_header("Cookie", cookie)
    try:
        url = urllib.request.urlopen(new_request)
        data = json.loads(url.read().decode())
        if fields_only:
            data = data[0]['fields']
        return data, 200
    except HTTPError as err:
        return {}, err.code


def get_synthesis(request):
    url = __get_pass_url__(request, 'etudiant')
    etudiant_data, etudiant_code = __make_json_request__(request, url, fields_only=True)
    if etudiant_code == 200:
        for taf in ['tafA2', 'tafA3']:
            if etudiant_data[taf] == 'null':
                etudiant_data[taf] = '-'
            else:
                taf_url = __get_pass_url__(request, 'taf/'+str(etudiant_data[taf]))
                taf_data, taf_code = __make_json_request__(request, taf_url, fields_only=True)
                return JsonResponse(taf_data, status=taf_code)
    return JsonResponse(etudiant_data, status=etudiant_code)
