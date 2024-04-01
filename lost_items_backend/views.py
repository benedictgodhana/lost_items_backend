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
from lostitems.models import LostItem, Claim
from .utils import compare_names
from django.contrib.auth import logout


def csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})


@csrf_exempt
def logout_view(request):
    logout(request)
    return JsonResponse({'message': 'Logout successful'})

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



def user_count(request):
    if request.method == 'GET':
        # Retrieve the count of registered users
        user_count = User.objects.count()

        # Return the count as JSON response
        return JsonResponse({'user_count': user_count})
    else:
        # Return an error for other HTTP methods
        return JsonResponse({'message': 'Method not allowed'}, status=405)

   
@csrf_exempt
def claim_lost_item(request):
    if request.method == 'POST':
        # Retrieve data from JSON payload
        data = request.POST.dict()

        # Retrieve claimant_name, lost_item_id, description, and is_verified from the data
        claimant_name = data.get('claimant_name')
        lost_item_id = data.get('lost_item')
        description = data.get('description')
        is_verified = data.get('is_verified')

        # Ensure that required fields are provided
        if claimant_name and lost_item_id:
            try:
                # Retrieve the LostItem object associated with the provided lost_item_id
                lost_item = LostItem.objects.get(id=lost_item_id)

                # Fetch all lost items and their owners
                lost_items = LostItem.objects.all()
                lost_item_owners = {item.id: item.owner for item in lost_items}

                # Compare claimant's name with the owner of the lost item
                matching_items = compare_names(claimant_name, lost_item_owners)
                
                if lost_item_id in matching_items:
                    # Create a new Claim object if the names match
                    claim = Claim.objects.create(
                        lost_item=lost_item,
                        claimant_name=claimant_name,
                        claimant_contact=request.user.email,  # Assuming the claimant's email is used as the claimant contact
                        description=description,
                        is_verified=is_verified if is_verified else False  # Set is_verified based on the provided value
                    )

                    # Return a success response
                    return JsonResponse({'message': 'Claim request received'})
                else:
                    # Return an error response if claimant's name does not match the owner
                    return JsonResponse({'error': 'Claimant does not match the owner of the lost item'}, status=400)
            except LostItem.DoesNotExist:
                # Handle the case where the LostItem with the provided ID does not exist
                return JsonResponse({'error': 'Lost item not found'}, status=404)
            except Exception as e:
                # Handle other exceptions
                return JsonResponse({'error': str(e)}, status=500)
        else:
            # Return an error response if required fields are missing
            return JsonResponse({'error': 'Claimant name and lost item ID are required'}, status=400)
    else:
        # Return an error response for other request methods
        return JsonResponse({'error': 'Method not allowed'}, status=405)
