from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date

# --- REQUIREMENT 1 & 2: User Profile Data ---
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Specific fields requested in PDF
    household_size = models.PositiveIntegerField(default=1, help_text="Number of people in the household")
    dietary_preferences = models.CharField(max_length=200, blank=True, help_text="e.g., Vegetarian, Vegan, Halal")
    budget_range = models.CharField(max_length=100, default="Medium", choices=[
        ('Low', 'Budget-Friendly'), 
        ('Medium', 'Standard'), 
        ('High', 'Premium')
    ])
    location = models.CharField(max_length=100, blank=True, help_text="City or Region")

    def __str__(self):
        return f"{self.user.username}'s Profile"

# Signal to auto-create a Profile when a User registers
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# --- REQUIREMENT 3: Inventory Item ---
class FoodItem(models.Model):
    CATEGORIES = [
        ('Dairy', 'Dairy'), ('Fruits', 'Fruits'),
        ('Vegetables', 'Vegetables'), ('Meat', 'Meat'),
        ('Grains', 'Grains'), ('Snacks', 'Snacks'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORIES)
    quantity = models.IntegerField(default=1)
    expiry_date = models.DateField()
    cost_per_unit = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    receipt_image = models.ImageField(upload_to='receipts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def days_remaining(self):
        return (self.expiry_date - date.today()).days

    @property
    def status_color(self):
        days = self.days_remaining
        if days < 0: return 'danger'
        if days <= 3: return 'warning'
        return 'success'

# --- REQUIREMENT 4: Resources ---
class Resource(models.Model):
    # Update choices to include 'Recipe'
    TYPE_CHOICES = [
        ('Article', 'Article'), 
        ('Video', 'Video'), 
        ('Recipe', 'Recipe')  # <--- Added this
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    url = models.URLField()
    category = models.CharField(max_length=50) 
    resource_type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    def __str__(self):
        return self.title
class ConsumptionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # 1. The Link: Connects to Inventory, but keeps log if Item is deleted
    source_item = models.ForeignKey(
        FoodItem, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='consumption_logs'
    )
    
    # 2. The Snapshot: Stores data permanently even if Source Item is deleted
    food_name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    quantity = models.IntegerField()
    date_consumed = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Ate {self.quantity} x {self.food_name}"