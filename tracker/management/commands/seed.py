# tracker/management/commands/seed_data.py

from django.core.management.base import BaseCommand
from tracker.models import FoodItem, Resource
from django.contrib.auth.models import User
from datetime import date, timedelta
import random

class Command(BaseCommand):
    help = 'Seeds the database with Bangladesh-relevant Food Items & Resources (Demo Ready!)'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting Bangladesh-style database seeding...")

        # 1. Create or get demo user
        user, created = User.objects.get_or_create(username='demo_user')
        if created:
            user.set_password('password123')
            user.email = 'demo@ecofridge.com'
            user.save()
            self.stdout.write("   Created demo_user (login: demo_user / password123)")

        # 2. Clear old food items
        FoodItem.objects.all().delete()

        # 3. Raw Food Items (Bangla + English names)
        food_data = [
            ("Dudh (Milk)", "Dairy", 1),
            ("Cha Milk Powder (Milk Powder)", "Dairy", 180),
            ("Doi (Yogurt)", "Dairy", 6),
            ("Ghee", "Dairy", 120),
            ("Dim (Eggs)", "Dairy", 18),

            ("Rui Maach (Rohu Fish)", "Meat", 1),
            ("Ilish Maach (Hilsa Fish)", "Meat", 0),
            ("Pangash Maach (Pangas Fish)", "Meat", 2),
            ("Telapia Maach (Tilapia Fish)", "Meat", 2),
            ("Beef (Raw Beef)", "Meat", 2),
            ("Mutton (Raw Mutton)", "Meat", 3),
            ("Chicken (Raw Chicken)", "Meat", 2),
            ("Chingri (Prawn/Shrimp)", "Meat", 1),

            ("Aloo (Potato)", "Vegetables", 25),
            ("Piyaj (Onion)", "Vegetables", 30),
            ("Roshun (Garlic)", "Vegetables", 45),
            ("Ada (Ginger)", "Vegetables", 20),
            ("Shak (Spinach/Red Amaranth)", "Vegetables", 1),
            ("Lao (Bottle Gourd)", "Vegetables", 5),
            ("Kumro (Pumpkin)", "Vegetables", 15),
            ("Begun (Brinjal/Eggplant)", "Vegetables", 4),
            ("Barbati (Yardlong Bean)", "Vegetables", 3),
            ("Dherosh (Okra/Ladyfinger)", "Vegetables", 3),
            ("Potol (Pointed Gourd)", "Vegetables", 5),
            ("Kacha Kola (Green Banana)", "Vegetables", 4),

            ("Kola (Banana)", "Fruits", 3),
            ("Aam (Mango)", "Fruits", 5),
            ("Peyara (Guava)", "Fruits", 7),
            ("Lebu (Lemon/Lime)", "Fruits", 20),
            ("Kamranga (Star Fruit)", "Fruits", 6),
            ("Anarosh (Pineapple)", "Fruits", 4),
            ("Dalim (Pomegranate)", "Fruits", 10),

            ("Chal (Rice)", "Grains", 365),
            ("Dal (Lentils - Masoor/Moong)", "Grains", 240),
            ("Mug Dal (Mung Beans)", "Grains", 240),
            ("Atta (Wheat Flour)", "Grains", 90),
            ("Suji (Semolina)", "Grains", 180),

            ("Chanachur (Spicy Mixture)", "Snacks", 90),
            ("Biscuits", "Snacks", 120),
            ("Muri (Puffed Rice)", "Snacks", 180),
            ("Chira (Flattened Rice)", "Snacks", 365),
            ("Noodles", "Snacks", 240),
            ("Achar (Pickle)", "Snacks", 365),

            ("Tel (Cooking Oil)", "Others", 180),
            ("Morich Gura (Chili Powder)", "Others", 365),
            ("Holud Gura (Turmeric Powder)", "Others", 365),
            ("Cha Pata (Tea Leaves)", "Others", 365),
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

        self.stdout.write(f"   Seeded {len(food_data)} Bangladesh-relevant food items!")

        # 4. Keep your original 20 resources (no change needed)
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

        self.stdout.write(self.style.SUCCESS('Database Seeded Successfully!'))
        self.stdout.write(self.style.SUCCESS('   Login: demo_user | Password: password123'))