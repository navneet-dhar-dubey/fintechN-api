import random
from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth.models import User
from api.models import Category, Transaction

class Command(BaseCommand):
    help = 'Populates the database with a set of realistic test data.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting database seeding process...'))

        # --- Clean up existing data ---
        # We delete non-superuser accounts to start fresh
        User.objects.filter(is_superuser=False).delete()
        Category.objects.all().delete()
        Transaction.objects.all().delete()
        self.stdout.write('Existing data cleared.')

        fake = Faker()

        # --- Create Users ---
        users = []
        for _ in range(5): # Create 5 new users
            username = fake.user_name()
            password = 'password123'
            user = User.objects.create_user(username=username, password=password, email=fake.email())
            users.append(user)
        self.stdout.write(f'{len(users)} users created.')

        # --- Create Categories and Transactions for each user ---
        default_categories = ['Groceries', 'Rent', 'Transport', 'Salary', 'Entertainment', 'Utilities']
        
        for user in users:
            # Create default categories for the user
            user_categories = [Category.objects.create(name=cat_name, user=user) for cat_name in default_categories]
            
            # Create 20-50 random transactions for the user for the current year
            for _ in range(random.randint(20, 50)):
                Transaction.objects.create(
                    user=user,
                    category=random.choice(user_categories),
                    type=random.choice(['INCOME', 'EXPENSE']),
                    amount=random.uniform(5.0, 500.0),
                    date=fake.date_this_year(),
                    description=fake.sentence(nb_words=6)
                )
        
        self.stdout.write('Categories and Transactions created for each user.')
        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully!'))