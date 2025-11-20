from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import FoodItem , Resource , Profile , ConsumptionLog
from .forms import FoodItemForm ,ProfileForm
from django.shortcuts import render, redirect
from datetime import date, timedelta

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

# tracker/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone # Import timezone
from datetime import date       # Import date

from .forms import FoodItemForm, ProfileForm
from .models import FoodItem, Resource, Profile, ConsumptionLog

# ... (Keep home and register views as they are) ...

# --- UPDATED DASHBOARD (Requirement 3 & 5) ---
@login_required
def dashboard(request):
    # 1. BASE QUERY
    # Start with all items belonging to this user
    items = FoodItem.objects.filter(user=request.user).order_by('expiry_date')
    
    # 2. FILTER LOGIC (This is what was missing!)
    cat_filter = request.GET.get('category')
    status_filter = request.GET.get('status')

    # Filter by Category (e.g., Dairy)
    if cat_filter:
        items = items.filter(category=cat_filter)
    
    # Filter by Status (e.g., Expired) using Python list comprehension
    # Note: This converts the QuerySet to a List, so it must be done last
    if status_filter == 'expired':
        items = [i for i in items if i.days_remaining < 0]
    elif status_filter == 'soon':
        items = [i for i in items if 0 <= i.days_remaining <= 3]

    # 3. WASTE RESCUE LOGIC (Requirement 5)
    # We need a fresh query for this so filters don't hide these important alerts
    fresh_items = FoodItem.objects.filter(user=request.user)
    expiring_items = fresh_items.filter(expiry_date__range=[date.today(), date.today() + timedelta(days=3)])
    expiring_categories = expiring_items.values_list('category', flat=True).distinct()
    
    rescue_recipes = Resource.objects.filter(
        category__in=expiring_categories, 
        resource_type='Recipe'
    )[:3]

    # 4. SMART RECOMMENDATIONS
    user_categories = fresh_items.values_list('category', flat=True).distinct()
    # Exclude recipes we already showed in "Waste Rescue" to keep it fresh
    general_resources = Resource.objects.filter(category__in=user_categories).exclude(id__in=rescue_recipes.values('id'))[:3]

    # 5. STATS CALCULATIONS
    # Must query DB again (all_items) to get accurate totals for the top cards
    # regardless of what filters are currently active on the table.
    all_items = FoodItem.objects.filter(user=request.user)
    
    context = {
        'items': items,                      # Filtered list (for the Table)
        'rescue_recipes': rescue_recipes,    # "Act Now" recipes
        'resources': general_resources,      # General Tips
        'recent_logs': ConsumptionLog.objects.filter(user=request.user).order_by('-date_consumed')[:3],
        'total': all_items.count(),
        'expired_count': sum(1 for i in all_items if i.days_remaining < 0),
        'soon_count': sum(1 for i in all_items if 0 <= i.days_remaining <= 3),
        'current_filter': cat_filter or status_filter # Helps highlight the active button
    }
    return render(request, 'tracker/dashboard.html', context)

@login_required
def delete_image(request, pk):
    item = get_object_or_404(FoodItem, pk=pk, user=request.user)
    
    if item.receipt_image:
        # delete(save=True) removes the file from disk AND saves the model with the field empty
        item.receipt_image.delete(save=True)
        messages.success(request, "Receipt image removed successfully.")
    else:
        messages.warning(request, "No image to delete.")
        
    return redirect('upload_image', pk=pk)

@login_required
def resources(request):
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


# Add this new function
def home(request):
    # If user is already logged in, send them straight to the app
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'tracker/home.html')

@login_required
def upload_image(request, pk):
    item = get_object_or_404(FoodItem, pk=pk, user=request.user)
    
    if request.method == 'POST':
        # Check if a file was actually sent
        if 'receipt_image' in request.FILES:
            item.receipt_image = request.FILES['receipt_image']
            item.save()
            messages.success(request, f"Image uploaded for {item.name}!")
            return redirect('dashboard')
        else:
            messages.warning(request, "No image selected.")
            
    return render(request, 'tracker/upload_image.html', {'item': item})