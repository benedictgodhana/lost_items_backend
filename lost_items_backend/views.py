from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.middleware.csrf import get_token
from django.contrib.auth import get_user_model
import json


def csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})


@csrf_exempt
def login(request):
    if request.method == 'POST':
        # Retrieve data from the POST request
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        
        # Authenticate user using email
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            # User is authenticated, login
            auth_login(request, user)
            return JsonResponse({'message': 'Login successful'})
        else:
            # Authentication failed
            return JsonResponse({'message': 'Invalid email or password'}, status=401)
    else:
        # Return an error for other HTTP methods
        return JsonResponse({'message': 'Method not allowed'}, status=405)
        
@csrf_exempt
def register(request):
    if request.method == 'POST':
        # Retrieve data from the POST request
        data = json.loads(request.body)
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        profile_picture = data.get('profile_picture')  # New field for profile picture
        
        # Create a new user
        User = get_user_model()
        try:
            # Attempt to create the user
            user = User.objects.create_user(username=username, email=email, password=password)
            
            # Update user profile picture if provided
            if profile_picture:
                user.profile_picture = profile_picture
                user.save()
                
            return JsonResponse({'message': 'Registration successful'})
        except Exception as e:
            # Handle any errors that occur during user creation
            return JsonResponse({'message': str(e)}, status=400)
    else:
        # Return an error for other HTTP methods
        return JsonResponse({'message': 'Method not allowed'}, status=405)


@csrf_exempt
def registered_users(request):
    if request.method == 'GET':
        # Retrieve all users from the database
        User = get_user_model()
        users = User.objects.all()

        # Serialize user data
        user_data = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]

        # Return the serialized user data as JSON response
        return JsonResponse({'users': user_data})
    else:
        # Return an error for other HTTP methods
        return JsonResponse({'message': 'Method not allowed'}, status=405)
