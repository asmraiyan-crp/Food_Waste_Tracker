from django.core.management.base import BaseCommand
from tracker.models import FoodItem, Resource
from django.contrib.auth.models import User
from datetime import date, timedelta
import random

class Command(BaseCommand):
    help = 'Seeds the database with Hackathon Part 1 Data (20 Items + 20 Resources)'

    def handle(self, *args, **kwargs):
        self.stdout.write("🌱 Seeding data...")

        # 1. Ensure we have a user to attach items to
        user, created = User.objects.get_or_create(username='demo_user')
        if created:
            user.set_password('password123')
            user.save()
            self.stdout.write("   - Created 'demo_user' (password: password123)")

        # 2. Seed 20 Food Items (Requirement: 15-20 relevant entries)
        # We mix expired, expiring soon, and fresh items for the "Smart Insights" UI
        food_data = [
            ("Milk", "Dairy", 3), ("Cheddar Cheese", "Dairy", 15), ("Yogurt", "Dairy", 5),
            ("Apples", "Fruits", 10), ("Bananas", "Fruits", -2), ("Grapes", "Fruits", 4),
            ("Carrots", "Vegetables", 7), ("Spinach", "Vegetables", 2), ("Potatoes", "Vegetables", 30),
            ("Chicken Breast", "Meat", 3), ("Ground Beef", "Meat", -1), ("Salmon", "Meat", 2),
            ("Rice", "Grains", 365), ("Pasta", "Grains", 365), ("Bread", "Grains", 4),
            ("Chips", "Snacks", 60), ("Cookies", "Snacks", 30), ("Nuts", "Snacks", 90),
            ("Orange Juice", "Fruits", 10), ("Lettuce", "Vegetables", 3)
        ]

        # Clear old data to prevent duplicates
        FoodItem.objects.all().delete()
        
        for name, cat, days in food_data:
            expiry = date.today() + timedelta(days=days)
            FoodItem.objects.create(
                user=user,
                name=name,
                category=cat,
                quantity=random.randint(1, 5),
                expiry_date=expiry
            )
        self.stdout.write(f"   - Seeded {len(food_data)} Food Items.")

        # 3. Seed 20 Resources (Requirement: 15-20 resources mapped to themes)
        resource_data = [
            ("How to Store Milk", "Dairy", "Article"),
            ("Can you freeze cheese?", "Dairy", "Video"),
            ("Creative uses for sour milk", "Dairy", "Article"),
            ("Yogurt storage hacks", "Dairy", "Article"),
            ("Keep Apples Crisp", "Fruits", "Video"),
            ("Banana Bread Recipe (Zero Waste)", "Fruits", "Article"),
            ("Freezing Berries Guide", "Fruits", "Article"),
            ("Regrow Green Onions", "Vegetables", "Video"),
            ("Keep Lettuce Fresh for Weeks", "Vegetables", "Article"),
            ("Root Vegetable Storage", "Vegetables", "Article"),
            ("Freezing Raw Meat Safely", "Meat", "Article"),
            ("Understanding Meat Expiry Labels", "Meat", "Video"),
            ("Leftover Chicken Recipes", "Meat", "Article"),
            ("Pantry Moth Prevention", "Grains", "Article"),
            ("Rice Storage 101", "Grains", "Video"),
            ("Revive Stale Bread", "Grains", "Article"),
            ("Healthy Snack Portions", "Snacks", "Article"),
            ("Eco-friendly Snack Packaging", "Snacks", "Video"),
            ("Composting 101", "Vegetables", "Article"),
            ("Understanding 'Best By' vs 'Use By'", "Dairy", "Article"),
        ]

        Resource.objects.all().delete()

        for title, cat, rtype in resource_data:
            Resource.objects.create(
                title=title,
                description=f"Learn sustainable habits for {cat}. Reduce waste and save money.",
                url="https://www.un.org/sustainabledevelopment/sustainable-consumption-production/",
                category=cat,
                resource_type=rtype
            )
        self.stdout.write(f"   - Seeded {len(resource_data)} Resources.")

        self.stdout.write(self.style.SUCCESS('✅ Database Seeded Successfully!'))