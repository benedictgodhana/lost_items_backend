from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Specify password field as write-only

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']  # Include password field

    def create(self, validated_data):
        # Create a new user instance with the validated data
        user = User.objects.create_user(**validated_data)
        return user
