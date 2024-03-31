from rest_framework import viewsets
from rest_framework.response import Response
from .models import LostItem
from .serializers import LostItemSerializer
from django.middleware.csrf import get_token
from django.http import JsonResponse




def csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})


class LostItemViewSet(viewsets.ModelViewSet):
    queryset = LostItem.objects.all()
    serializer_class = LostItemSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        # Do whatever processing you need here

        return Response(data)