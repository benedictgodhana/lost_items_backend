from rest_framework import serializers
from .models import LostItem
from .models import Claim

class LostItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LostItem
        fields = '__all__'  # Ensure 'image' field is included




class ClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        fields = ['id', 'lost_item', 'claimant_name','claimant_contact', 'description','claim_date', 'is_verified']
