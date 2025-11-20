# tracker/management/commands/seed_data.py

from django.core.management.base import BaseCommand
from tracker.models import FoodItem, Resource
from django.contrib.auth.models import User
from datetime import date, timedelta
import random

class Command(BaseCommand):
    help = 'Seeds the database with realistic Food Items & Resources (Demo Ready!)'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting Food Seeder...")

        # 1. Create or get demo user
        user, created = User.objects.get_or_create(username='demo_user')
        if created:
            user.set_password('password123')
            user.email = 'demo@ecofridge.com'
            user.save()
            self.stdout.write("   Created demo_user (login: demo_user / password123)")

        # 2. Clear old food items
        FoodItem.objects.all().delete()

        # 3. Raw Food Items — English first, Bangla in brackets
        food_data = [
            ("Milk (Dudh)", "Dairy", 1),
            ("Milk Powder (Cha Milk Powder)", "Dairy", 180),
            ("Yogurt (Doi)", "Dairy", 6),
            ("Ghee", "Dairy", 120),
            ("Eggs (Dim)", "Dairy", 18),

            ("Rohu Fish (Rui Maach)", "Meat", 1),
            ("Hilsa Fish (Ilish Maach)", "Meat", 0),
            ("Pangas Fish (Pangash Maach)", "Meat", 2),
            ("Tilapia Fish (Telapia Maach)", "Meat", 2),
            ("Beef (Raw Beef)", "Meat", 2),
            ("Mutton (Raw Mutton)", "Meat", 3),
            ("Chicken (Raw Chicken)", "Meat", 2),
            ("Prawn/Shrimp (Chingri)", "Meat", 1),

            ("Potato (Aloo)", "Vegetables", 25),
            ("Onion (Piyaj)", "Vegetables", 30),
            ("Garlic (Roshun)", "Vegetables", 45),
            ("Ginger (Ada)", "Vegetables", 20),
            ("Spinach/Red Amaranth (Shak)", "Vegetables", 1),
            ("Bottle Gourd (Lao)", "Vegetables", 5),
            ("Pumpkin (Kumro)", "Vegetables", 15),
            ("Eggplant (Begun)", "Vegetables", 4),
            ("Yardlong Bean (Barbati)", "Vegetables", 3),
            ("Okra (Dherosh)", "Vegetables", 3),
            ("Pointed Gourd (Potol)", "Vegetables", 5),
            ("Green Banana (Kacha Kola)", "Vegetables", 4),

            ("Banana (Kola)", "Fruits", 3),
            ("Mango (Aam)", "Fruits", 5),
            ("Guava (Peyara)", "Fruits", 7),
            ("Lemon/Lime (Lebu)", "Fruits", 20),
            ("Star Fruit (Kamranga)", "Fruits", 6),
            ("Pineapple (Anarosh)", "Fruits", 4),
            ("Pomegranate (Dalim)", "Fruits", 10),

            ("Rice (Chal)", "Grains", 365),
            ("Lentils (Dal - Masoor/Moong)", "Grains", 240),
            ("Mung Beans (Mug Dal)", "Grains", 240),
            ("Wheat Flour (Atta)", "Grains", 90),
            ("Semolina (Suji)", "Grains", 180),

            ("Spicy Mixture (Chanachur)", "Snacks", 90),
            ("Biscuits", "Snacks", 120),
            ("Puffed Rice (Muri)", "Snacks", 180),
            ("Flattened Rice (Chira)", "Snacks", 365),
            ("Noodles", "Snacks", 240),
            ("Pickle (Achar)", "Snacks", 365),

            ("Cooking Oil (Tel)", "Others", 180),
            ("Chili Powder (Morich Gura)", "Others", 365),
            ("Turmeric Powder (Holud Gura)", "Others", 365),
            ("Tea Leaves (Cha Pata)", "Others", 365),
        ]

        for name, category, days in food_data:
            expiry = date.today() + timedelta(days=days)
            FoodItem.objects.create(
                user=user,
                name=name,
                category=category,
                quantity=random.randint(1, 6),
                expiry_date=expiry
            )

        self.stdout.write(f"   Seeded {len(food_data)} food items (English + Bangla)")

        # 4. Resources (unchanged)
        Resource.objects.all().delete()
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

        for title, cat, rtype in resource_data:
            Resource.objects.create(
                title=title,
                description=f"Learn sustainable habits for {cat}. Reduce waste and save money.",
                url="https://www.un.org/sustainabledevelopment/sustainable-consumption-production/",
                category=cat,
                resource_type=rtype
            )
        self.stdout.write(f"   Seeded {len(resource_data)} Resources.")

        self.stdout.write(self.style.SUCCESS('Food Seeder Completed Successfully!'))
        self.stdout.write(self.style.SUCCESS('   Login → Username: demo_user | Password: password123'))