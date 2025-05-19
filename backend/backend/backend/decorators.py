# backend/decorators.py
import jwt
from django.http import JsonResponse
from functools import wraps
from django.conf import settings
def token_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        auth_header = request.META.get('HTTP_AUTHORIZATION')  # <-- Usa esto
        print("Auth Header:", auth_header)

        if not auth_header:
            return JsonResponse({'error': 'Authorization header missing'}, status=401)
        try:
            prefix, token = auth_header.split(' ')
            if prefix != 'Bearer':
                return JsonResponse({'error': 'Invalid token prefix'}, status=401)

            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            print("Payload decoded:", payload)
            request.user_id = payload.get('user_id')
            request.user_rol = payload.get('rol')
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
            return JsonResponse({'error': 'Invalid or expired token'}, status=401)

        return view_func(request, *args, **kwargs)
    return _wrapped_view

