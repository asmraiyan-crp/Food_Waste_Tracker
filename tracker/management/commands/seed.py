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
            ("How to Store Milk", "Dairy", "Article","https://dairyfarmersofcanada.ca/en/canadian-goodness/articles/freeze-store-milk"),
            ("Freezing Cheese Guide", "Dairy", "Video","https://youtu.be/WEIElFEZd-Q?si=Wf1WvLdJzstP209-"),
            ("Keep Leafy Greens Fresh", "Vegetables", "Article","https://food-guide.canada.ca/en/cooking-skills/storing-leafy-greens/"),
            ("Regrow Green Onions", "Vegetables", "Video","https://youtu.be/kfTr9nYogW8?si=X7_nRKlBtZmFDchw"),
            ("Root Veggie Storage", "Vegetables", "Article","https://yardandgarden.extension.iastate.edu/how-to/storing-winter-storage-vegetables"),
            ("Banana Storage Hacks", "Fruits", "Video","https://youtu.be/-visWu3V0gA?si=LPkDB3abzAMGL1TB"),
            ("Freezing Berries", "Fruits", "Article","https://extension.umd.edu/resource/berry-good-guide-freezing-berries-year-round-enjoyment/"),
            ("Meat Safety 101", "Meat", "Article","https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics"),
            ("Understanding Expiry Labels", "Meat", "Video","https://youtu.be/vZJIQ40eUyk?si=LBlMMB_8_HeHtmkl"),
            ("Pantry Moth Prevention", "Grains", "Article","https://www.realsimple.com/how-to-prevent-pantry-moths-11685751"),
            ("Rice Storage Tips", "Grains", "Video","https://youtu.be/yR7maPU7cTM?si=AU2mgzn-ezUIBn3l"),
            ("Zero Waste Cooking", "Vegetables", "Article","https://zerowastechef.com/"),
            ("Composting Basics", "Vegetables", "Video","https://youtu.be/4Fskb_7z86M?si=bRWa0fAfqV1WjCeN"),
            ("Meal Planning on a Budget", "Grains", "Article","https://www.bbcgoodfood.com/feature/budget"),
            ("Leftover Makeovers", "Meat", "Article","https://hgic.clemson.edu/leftover-makeover/"),
        ]

        for title, cat, rtype, urls in resource_data:
            Resource.objects.create(
                title=title,
                description=f"Learn how to extend the shelf life of {cat} and reduce waste.",
                url=urls,
                category=cat,
                resource_type=rtype
            )
        self.stdout.write(f"   - Seeded {len(resource_data)} Resources")

        recipe_data = [
            ("Sour Milk Pancakes", "Dairy", "Recipe"),
            ("Banana Bread (Overripe)", "Fruits", "Recipe"),
            ("Vegetable Scrap Stock", "Vegetables", "Recipe"),
            ("Bread Pudding (Stale Bread)", "Grains", "Recipe"),
            ("Fried Rice (Leftover Rice)", "Grains", "Recipe"),
            ("Smoothie Packs (Dying Fruit)", "Fruits", "Recipe"),
        ]

        for title, cat, rtype in recipe_data:
            Resource.objects.create(
                title=title,
                description=f"Don't throw it away! Use your expiring {cat} to make this delicious meal.",
                url="https://www.allrecipes.com/recipes/17570/everyday-cooking/more-meal-ideas/leftovers/",
                category=cat,
                resource_type=rtype
            )
        self.stdout.write(f"   - Seeded {len(recipe_data)} Recipes")

        self.stdout.write(self.style.SUCCESS('✅ Database Seeded Successfully!'))