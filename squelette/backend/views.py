import json
import urllib.request

from django.core import serializers
from django.http import HttpResponse, JsonResponse

tmdb_key = "70b985ccb055e09129a4adb356172eba"


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. This is the back-end !")


def actor(request, name, surname):
    actor_url = "https://api.themoviedb.org/3/search/person?api_key={}&language=en-US&query={}%20{}&page=1&include_adult=false".format(tmdb_key, name, surname)
    with urllib.request.urlopen(actor_url) as url:
        data = json.loads(url.read().decode())
        results = data['results']
        if len(results) > 0:
            actor_id = results[0]['id']
        else:
            return JsonResponse([], safe=False)

    movies_url = "https://api.themoviedb.org/3/discover/movie?api_key={}&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1&with_cast={}".format(tmdb_key, actor_id)
    with urllib.request.urlopen(movies_url) as url:
        data = json.loads(url.read().decode())
        movies = [movie['original_title'] for movie in data['results']]
    return JsonResponse(movies, safe=False)


def get_synthese(request):
    etudiant_url = 'http://127.0.0.1:8000/pass/etudiant'
    new_request = urllib.request.Request(etudiant_url)
    new_request.add_header("Cookie", "cookie1="+request.headers.get('Cookie'))
    with urllib.request.urlopen(new_request) as url:
        data = json.loads(url.read().decode())
        data = serializers.serialize('json', url.read().decode())
        print(data)
        data = data[0]
        print(data)
        return JsonResponse(data, safe=False)
