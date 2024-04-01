from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import LostItem, Claim  # Import the Claim model
from .serializers import LostItemSerializer, ClaimSerializer  # Import the Claim serializer
from django.middleware.csrf import get_token
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .utils import compare_names
from django.shortcuts import get_object_or_404

def csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})

class LostItemViewSet(viewsets.ModelViewSet):
    queryset = LostItem.objects.all()
    serializer_class = LostItemSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClaimViewSet(viewsets.ModelViewSet):
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def total_lost_items(request):
    total_items = LostItem.objects.count()
    return JsonResponse({'total_items': total_items})



def claim_lost_item(request):
    if request.method == 'POST':
        claimant_name = request.POST.get('claimant_name')  # Assuming claimant_name is submitted via POST
        lost_items = LostItem.objects.all()  # Fetch all lost items
        lost_item_owners = {item.id: item.owner for item in lost_items}  # Create a dictionary of lost item IDs and owners

        # Compare claimant's name with names of lost item owners
        matching_items = compare_names(claimant_name, lost_item_owners)

        if matching_items:
            # At least one matching lost item found
            # Fetch the name of the first matching item
            matching_item = get_object_or_404(LostItem, id=matching_items[0])
            matching_item_name = matching_item.name
            
            # Proceed with claim verification process
            # For demonstration purposes, let's create a new claim
            claim = Claim.objects.create(
                lost_item_id=matching_items[0],  # Assuming the first matching item is selected
                claimant_name=request.user.username,  # Assuming the claimant is authenticated and their username is used as the claimant name
                claimant_contact=request.user.email,  # Assuming the claimant's email is used as the claimant contact
                description=claimant_description,
                is_verified=False  # Initially set to False, you can update it based on your verification process
            )
            return JsonResponse({'message': f'Claim request received for {matching_item_name}'})
        else:
            # No matching lost item found
            return JsonResponse({'error': 'No matching lost item found'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)