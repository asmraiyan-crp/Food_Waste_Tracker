from django import forms
from .models import Profile, FoodItem

class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['name', 'category', 'quantity', 'expiry_date', 'cost_per_unit', 'receipt_image']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'})
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['household_size', 'dietary_preferences', 'budget_range', 'location']
        widgets = {
            'dietary_preferences': forms.TextInput(attrs={'placeholder': 'e.g. Vegetarian, Nut-free'}),
            'location': forms.TextInput(attrs={'placeholder': 'City/Area'}),
        }