from django.db import models
from django.contrib.auth.models import User  # Import the built-in User model
from django.conf import settings
from django.contrib.auth import get_user_model


class LostItem(models.Model):
    STATUS_CHOICES = [
        ('lost', 'Lost'),
        ('found', 'Found'),
        ('claimed', 'Claimed'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    date_found = models.DateField()
    owner = models.CharField(max_length=150)
    image = models.ImageField(upload_to='lost_item_images/')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='lost')

    def __str__(self):
        return self.name

class Claim(models.Model):
    lost_item = models.ForeignKey(LostItem, on_delete=models.CASCADE, related_name='claims')
    claimant_name = models.CharField(max_length=255)
    claimant_contact = models.CharField(max_length=255)  # Contact information of the claimant
    description = models.TextField()
    claim_date = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.lost_item}"
