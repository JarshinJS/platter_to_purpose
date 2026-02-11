from django.contrib import admin
from .models import FoodPost

@admin.register(FoodPost)
class FoodPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'donor', 'quantity', 'location', 'expiry_time', 'is_claimed', 'created_at')
    list_filter = ('is_claimed', 'created_at', 'donor')
    search_fields = ('title', 'description', 'location')
