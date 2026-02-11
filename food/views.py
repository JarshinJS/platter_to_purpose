from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import FoodPost
from .forms import FoodPostForm

def food_list(request):
    foods = FoodPost.objects.filter(is_claimed=False, expiry_time__gt=timezone.now()).order_by('-created_at')
    return render(request, 'food/food_list.html', {'foods': foods})

def food_detail(request, pk):
    food = get_object_or_404(FoodPost, pk=pk)
    return render(request, 'food/food_detail.html', {'food': food})

@login_required
def post_food(request):
    # Ensure only hotels can post
    if not request.user.role == 'HOTEL':
        return redirect('home')
    
    if request.method == 'POST':
        form = FoodPostForm(request.POST, request.FILES)
        if form.is_valid():
            food = form.save(commit=False)
            food.donor = request.user
            food.save()
            return redirect('dashboard')
    else:
        form = FoodPostForm()
    return render(request, 'food/food_post.html', {'form': form})
