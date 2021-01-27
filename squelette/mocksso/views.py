from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers

from django.contrib.auth import authenticate, login, logout

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. This is the SSO !")


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def do_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            data = serializers.serialize('json', [user], fields=["username"])
            response = HttpResponse(data, content_type='application/json', status=200)
            response['Authentification'] = str(request.session._get_or_create_session_key())
            return response
        else:
            return HttpResponse(status=401)
    return HttpResponse(status=405)

def get_user(request):
    if request.user.is_authenticated:
        response = serializers.serialize('json', [request.user], fields=["username"])
        return HttpResponse(response, status=200)
    else:
        return JsonResponse({}, status=404)

@csrf_exempt
def do_logout(request):
    logout(request)
    return HttpResponse(status=200)
    
