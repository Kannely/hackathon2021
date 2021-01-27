from django.conf import settings

class CORSMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.headers.get('Origin') is not None:
            response['Access-Control-Allow-Origin'] = request.headers.get('Origin')
        else:
            response['Access-Control-Allow-Origin'] = "*"
        response['Access-Control-Allow-Credentials'] = 'true'
        response['Access-Control-Expose-Headers'] = 'Authentification'
        return response
