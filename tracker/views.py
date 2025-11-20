from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import FoodItem
from .forms import FoodItemForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'tracker/register.html', {'form': form})

@login_required
def dashboard(request):
    items = FoodItem.objects.filter(user=request.user).order_by('expiry_date')
    context = {
        'items': items,
        'total': items.count(),
        'expired_count': sum(1 for i in items if i.days_remaining < 0),
        'soon_count': sum(1 for i in items if 0 <= i.days_remaining <= 3)
    }
    return render(request, 'tracker/dashboard.html', context)

@login_required
def add_item(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('dashboard')
    else:
        form = FoodItemForm()
    return render(request, 'tracker/form.html', {'form': form, 'title': 'Add Item'})

@login_required
def edit_item(request, pk):
    item = get_object_or_404(FoodItem, pk=pk, user=request.user)
    if request.method == 'POST':
        form = FoodItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = FoodItemForm(instance=item)
    return render(request, 'tracker/form.html', {'form': form, 'title': 'Edit Item'})

@login_required
def delete_item(request, pk):
    item = get_object_or_404(FoodItem, pk=pk, user=request.user)
    if request.method == 'POST':
        item.delete()
        return redirect('dashboard')
    return render(request, 'tracker/delete_confirm.html', {'item': item})

# Add this import at the top
from django.shortcuts import render, redirect

# Add this new function
def home(request):
    # If user is already logged in, send them straight to the app
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'tracker/home.html')