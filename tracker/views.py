from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import FoodItem , Resource , Profile , ConsumptionLog
from .forms import FoodItemForm ,ProfileForm

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

def resources(request):
    # Fetch all resources
    all_resources = Resource.objects.all()
    return render(request, 'tracker/resources.html', {'resources': all_resources})
    

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

@login_required
def profile(request):
    # Get or create profile to avoid errors
    profile_obj, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        p_form = ProfileForm(request.POST, instance=profile_obj)
        
        # Update basic User model fields
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        
        if p_form.is_valid():
            user.save()
            p_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
            
    else:
        p_form = ProfileForm(instance=profile_obj)

    return render(request, 'tracker/profile.html', {'p_form': p_form, 'user': request.user})


# --- REQUIREMENT 2: Log Consumption ---
@login_required
def log_food(request, pk):
    # Fetch the inventory item
    item = get_object_or_404(FoodItem, pk=pk, user=request.user)
    
    if request.method == 'POST':
        consumed_qty = 1 
        
        # Create the Log Entry with the dependency
        ConsumptionLog.objects.create(
            user=request.user,
            source_item=item,
            food_name=item.name,
            category=item.category,
            quantity=consumed_qty
        )
        
        # Update Inventory Logic
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
            messages.success(request, f"Logged 1 unit of {item.name}.")
        else:
            item.delete()
            messages.success(request, f"Finished {item.name}. Moved to history.")
            
        return redirect('dashboard')
        
    return render(request, 'tracker/log_confirm.html', {'item': item})

# --- REQUIREMENT 2: History Page ---
@login_required
def consumption_history(request):
    logs = ConsumptionLog.objects.filter(user=request.user).order_by('-date_consumed')
    return render(request, 'tracker/history.html', {'logs': logs})


# Add this import at the top
from django.shortcuts import render, redirect

# Add this new function
def home(request):
    # If user is already logged in, send them straight to the app
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'tracker/home.html')