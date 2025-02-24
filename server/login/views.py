# login/views.py

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('email')  # front-end calls it "email" but it's actually the username
            password = data.get('password')
        except:
            return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return JsonResponse({'success': True, 'message': 'Login successful'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid credentials'}, status=401)

    return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)


def check_auth_view(request):
    if request.user.is_authenticated:
        return JsonResponse({'isAuthenticated': True})
    else:
        return JsonResponse({'isAuthenticated': False})


@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        auth_logout(request)
        return JsonResponse({'success': True, 'message': 'Logged out successfully'})
    return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
