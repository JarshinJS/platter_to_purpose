from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    if request.user.role == 'HOTEL':
        # Show posts made by this hotel
        my_posts = request.user.food_posts.all()
        return render(request, 'dashboard/hotel_dashboard.html', {'my_posts': my_posts})
    else:
        # Show orders made by this orphanage
        my_orders = request.user.orders.all()
        return render(request, 'dashboard/orphanage_dashboard.html', {'my_orders': my_orders})
