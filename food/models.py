from django.db import models
from django.conf import settings

class FoodPost(models.Model):
    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='food_posts')
    title = models.CharField(max_length=200)
    description = models.TextField()
    quantity = models.PositiveIntegerField(help_text="Number of servings/meals")
    location = models.CharField(max_length=255) # Donor can specify pickup location if different from profile
    expiry_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_claimed = models.BooleanField(default=False)
    image = models.ImageField(upload_to='food_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.donor.username}"

    def get_rating_stars(self):
        if hasattr(self, 'order') and hasattr(self.order, 'feedback'):
            return "⭐" * self.order.feedback.rating
        return ""
