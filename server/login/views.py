from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username_input = data.get('email')  # frontend field
            password = data.get('password')
        except:
            return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)

        try:
            # First filter all users that match "username" (case-insensitive)
            user_qs = User.objects.filter(username__iexact=username_input)
            if user_qs.exists():
                user = user_qs.first()
                # ✅ Now check if the casing is exactly the same
                if user.username != username_input:
                    return JsonResponse({'success': False, 'message': 'Username casing mismatch'}, status=401)
                if user.check_password(password):
                    auth_login(request, user)
                    return JsonResponse({'success': True, 'message': 'Login successful'})
                else:
                    return JsonResponse({'success': False, 'message': 'Incorrect password'}, status=401)
            else:
                return JsonResponse({'success': False, 'message': 'User not found'}, status=401)
        except:
            return JsonResponse({'success': False, 'message': 'Login error'}, status=500)

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
