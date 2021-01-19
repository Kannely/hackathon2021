import json
import urllib.request

from django.http import HttpResponse, JsonResponse

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. This is PASS !")
