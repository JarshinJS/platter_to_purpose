from django.db import models
from django.conf import settings
from food.models import FoodPost
import uuid

class Order(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    food_post = models.OneToOneField(FoodPost, on_delete=models.CASCADE, related_name='order')
    claimed_at = models.DateTimeField(auto_now_add=True)
    secret_token = models.UUIDField(default=uuid.uuid4, editable=False)
    
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        CONFIRMED = 'CONFIRMED', 'Confirmed'
        COMPLETED = 'COMPLETED', 'Completed'

    status = models.CharField(max_length=20, default=Status.PENDING, choices=Status.choices)

    def __str__(self):
        return f"Order for {self.food_post.title} by {self.recipient.username}"

    def save(self, *args, **kwargs):
        # Automatically mark food as claimed upon creation
        if not self.pk:
            self.food_post.is_claimed = True
            self.food_post.save()
        super().save(*args, **kwargs)
