from rest_framework import serializers
from .models import LostItem

class LostItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LostItem
        fields = ['id', 'name', 'description', 'location', 'date_found', 'owner', 'image', 'status']

