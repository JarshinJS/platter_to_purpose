from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from orders.models import Order
from .forms import FeedbackForm
from django.contrib import messages

@login_required
def submit_feedback(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    
    # Only recipient can submit feedback
    if request.user != order.recipient:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.order = order
            feedback.save()
            messages.success(request, 'Thank you for your feedback!')
            return redirect('dashboard')
    else:
        form = FeedbackForm()
        
    return render(request, 'feedback/submit_feedback.html', {'form': form, 'order': order})

