from django.db import models
from django.contrib.auth.models import User  # Import the built-in User model

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
