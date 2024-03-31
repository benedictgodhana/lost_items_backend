from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models  # Ensure this line is included

class User(AbstractUser):
    # Add a unique related_name for groups
    groups = models.ManyToManyField(Group, related_name='user_groups')

    # Add a unique related_name for user_permissions
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='user_permissions_set',
        help_text=_('Specific permissions for this user.'),
        related_query_name='user',
    )
