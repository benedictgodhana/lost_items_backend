from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer

# views.py in the lostitems app

from django.middleware.csrf import get_token
from django.http import JsonResponse

def csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})

# Other views for your lostitems app if present

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
