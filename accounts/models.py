from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        HOTEL = 'HOTEL', 'Hotel'
        ORPHANAGE = 'ORPHANAGE', 'Orphanage'

    role = models.CharField(max_length=50, choices=Role.choices, default=Role.HOTEL)
    
    # Add any common fields like phone, address, etc. if needed
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    def is_hotel(self):
        return self.role == self.Role.HOTEL

    def is_orphanage(self):
        return self.role == self.Role.ORPHANAGE
