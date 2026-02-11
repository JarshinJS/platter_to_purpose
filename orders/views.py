from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from food.models import FoodPost
from .models import Order

import qrcode
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.conf import settings
from django.core.files.base import ContentFile
from io import BytesIO

from django.utils import timezone
from datetime import timedelta
from django.contrib import messages

@login_required
def claim_food(request, food_id):
    food = get_object_or_404(FoodPost, pk=food_id)
    if food.is_claimed:
        # Prevent double claiming
        return redirect('food_list')
    if request.method == 'POST':
        # Create order
        order = Order.objects.create(recipient=request.user, food_post=food)
        # Redirect to dashboard or confirmation
        return redirect('dashboard')
    
    return render(request, 'orders/claim_confirmation.html', {'food': food})

from django.core.exceptions import ValidationError

@login_required
def generate_qr(request, order_id):
    """
    Generates a QR code image for the given order's secret verification token.
    Only the Recipient (Orphanage) should be able to view/download this.
    """
    order = get_object_or_404(Order, pk=order_id)
    
    # Security check: Only the recipient can view their QR code
    if request.user != order.recipient:
        return HttpResponseForbidden("You are not authorized to view this QR code.")
    
    # Data to encode in QR (The secret token)
    # Could be a URL to verify: http://site.com/orders/verify/<token>/
    # Or just the raw token. Let's use a Verify URL for easier scanning.
    # verify_url = request.build_absolute_uri(f'/orders/verify/{order.secret_token}/')
    
    # let's just use the token for now, or a deep link
    data = str(order.secret_token)
    
    qr = qrcode.QRCode(
        version=None,  # Allow auto-sizing to fit the UUID
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return HttpResponse(buffer.getvalue(), content_type="image/png")

@login_required
def verify_pickup(request):
    """
    View for the Hotel (Donor) to verify the pickup by scanning/entering the code.
    """
    if request.method == 'POST':
        token = request.POST.get('token')
        try:
            order = Order.objects.get(secret_token=token)
            
            # Ensure the logged-in hotel is the one who donated this food
            if order.food_post.donor != request.user:
                 return render(request, 'orders/verify_pickup.html', {'error': 'This order does not belong to you.'})

            if order.status == Order.Status.COMPLETED:
                return render(request, 'orders/verify_pickup.html', {'error': 'Order already completed.'})
                
            # Verify Success
            order.status = Order.Status.COMPLETED
            order.save()
            return render(request, 'orders/verify_success.html', {'order': order})
            
        except (Order.DoesNotExist, ValidationError):
            return render(request, 'orders/verify_pickup.html', {'error': 'Invalid Token. Please try again.'})
            
    return render(request, 'orders/verify_pickup.html')

@login_required
def withdraw_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    
    # Permission Check
    if request.user != order.recipient:
        return HttpResponseForbidden("You cannot withdraw this order.")
        
    # Time window check (5 minutes)
    time_elapsed = timezone.now() - order.claimed_at
    if time_elapsed > timedelta(minutes=5):
        messages.error(request, "Cancellation period has expired (5 mins).")
        return redirect('dashboard')
        
    if request.method == 'POST':
        # Reset food status
        food = order.food_post
        food.is_claimed = False
        food.save()
        
        # Delete order
        order.delete()
        messages.success(request, "Order withdrawn successfully.")
        return redirect('dashboard')
        
    return render(request, 'orders/withdraw_confirm.html', {'order': order})
