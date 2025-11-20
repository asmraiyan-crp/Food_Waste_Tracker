from django.core.management.base import BaseCommand
from tracker.models import FoodItem, Resource, Profile
from django.contrib.auth.models import User
from datetime import date, timedelta
import random

class Command(BaseCommand):
    help = 'Seeds the database with Part 1 Requirements (Profiles, Foods, Resources)'

    def handle(self, *args, **kwargs):
        self.stdout.write("🌱 Starting Database Seeder...")

        # ---------------------------------------------------------
        # 1. Create Demo User & Profile (Requirement 1 & 2)
        # ---------------------------------------------------------
        user, created = User.objects.get_or_create(username='demo_user')
        if created:
            user.set_password('password123')
            user.email = 'demo@innovatex.com'
            user.first_name = "Rahim"
            user.last_name = "Ahmed"
            user.save()
            self.stdout.write("   - Created User: demo_user (password123)")
        
        # Update the Profile (Auto-created by signal, but we set values here)
        profile = Profile.objects.get(user=user)
        profile.household_size = 4
        profile.dietary_preferences = "Halal, Omnivore"
        profile.budget_range = "Medium"
        profile.location = "Mirpur, Dhaka"
        profile.save()
        self.stdout.write(f"   - Updated Profile: {profile.location}, {profile.household_size} members")

        # ---------------------------------------------------------
        # 2. Seed Food Inventory (Requirement 3)
        # ---------------------------------------------------------
        # Clear old data
        FoodItem.objects.filter(user=user).delete()

        food_data = [
            # (Name, Category, Days until expiry)
            ("Milk (Dudh)", "Dairy", 2),
            ("Yogurt (Doi)", "Dairy", 6),
            ("Eggs (Dim)", "Dairy", 12),
            ("Rohu Fish (Rui)", "Meat", 1),
            ("Chicken Breast", "Meat", 3),
            ("Beef (Gorur Mangsho)", "Meat", 2),
            ("Spinach (Palong Shak)", "Vegetables", 1),
            ("Potato (Aloo)", "Vegetables", 20),
            ("Onion (Piyaj)", "Vegetables", 30),
            ("Green Chilies", "Vegetables", 5),
            ("Lentils (Masoor Dal)", "Grains", 180),
            ("Rice (Miniket)", "Grains", 365),
            ("Banana (Sagor Kola)", "Fruits", 3),
            ("Mango", "Fruits", 5),
            ("Guava", "Fruits", 4),
            ("Chanachur", "Snacks", 60),
            ("Biscuits", "Snacks", 90),
            ("Mustard Oil", "Grains", 365),
            ("Turmeric Powder", "Grains", 365),
            ("Tea Leaves", "Snacks", 180),
        ]

        for name, cat, days in food_data:
            expiry = date.today() + timedelta(days=days)
            FoodItem.objects.create(
                user=user,
                name=name,
                category=cat,
                quantity=random.randint(1, 5),
                expiry_date=expiry,
                cost_per_unit=random.randint(50, 500)
            )
        self.stdout.write(f"   - Seeded {len(food_data)} Food Items")

        # ---------------------------------------------------------
        # 3. Seed Resources (Requirement 4)
        # ---------------------------------------------------------
        Resource.objects.all().delete()
        
        resource_data = [
            ("How to Store Milk", "Dairy", "Article"),
            ("Freezing Cheese Guide", "Dairy", "Video"),
            ("Keep Leafy Greens Fresh", "Vegetables", "Article"),
            ("Regrow Green Onions", "Vegetables", "Video"),
            ("Root Veggie Storage", "Vegetables", "Article"),
            ("Banana Storage Hacks", "Fruits", "Video"),
            ("Freezing Berries", "Fruits", "Article"),
            ("Meat Safety 101", "Meat", "Article"),
            ("Understanding Expiry Labels", "Meat", "Video"),
            ("Pantry Moth Prevention", "Grains", "Article"),
            ("Rice Storage Tips", "Grains", "Video"),
            ("Zero Waste Cooking", "Vegetables", "Article"),
            ("Composting Basics", "Vegetables", "Video"),
            ("Meal Planning on a Budget", "Grains", "Article"),
            ("Leftover Makeovers", "Meat", "Article"),
        ]

        for title, cat, rtype in resource_data:
            Resource.objects.create(
                title=title,
                description=f"Learn how to extend the shelf life of {cat} and reduce waste.",
                url="https://www.fao.org/food-loss-and-food-waste/flw-data)",
                category=cat,
                resource_type=rtype
            )
        self.stdout.write(f"   - Seeded {len(resource_data)} Resources")

        self.stdout.write(self.style.SUCCESS('✅ Database Seeded Successfully!'))