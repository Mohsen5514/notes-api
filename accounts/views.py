from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        data=json.loads(request.body)
        username=data.get('username')
        password=data.get('password')
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error':'username already exist'},status=400)
        user=User.objects.create_user(username=username,password=password)
        return JsonResponse({'message':'user registered successfully','user_id':user.id})
    
@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data=json.loads(request.body)
        username=data.get('username')
        password=data.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return JsonResponse({'message':'login successfully'})
        else:
            return JsonResponse({'message':'Invalid credentials'},status=400)
        
def logout_user(request):
    logout(request)
    return JsonResponse({'message':'logged out successfully'})

