from django.db import models
from django.contrib.auth.models import User
from datetime import date

class FoodItem(models.Model):
    # ... existing fields ...
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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def days_remaining(self):
        return (self.expiry_date - date.today()).days

    # --- ADD THIS NEW PROPERTY ---
    @property
    def days_past_due(self):
        return abs(self.days_remaining)

    @property
    def status_color(self):
        days = self.days_remaining
        if days < 0: return 'danger'
        if days <= 3: return 'warning'
        return 'success'
# Append this to tracker/models.py

class Resource(models.Model):
    TYPE_CHOICES = [('Article', 'Article'), ('Video', 'Video')]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    url = models.URLField()
    # Matches FoodItem category for the "Basic Tracking Logic" requirement
    category = models.CharField(max_length=50) 
    resource_type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    def __str__(self):
        return self.title