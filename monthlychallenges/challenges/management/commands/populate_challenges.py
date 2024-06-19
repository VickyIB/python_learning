# challenges/management/commands/populate_challenges.py
from django.core.management.base import BaseCommand
from challenges.models import MonthlyChallenge
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Populate the MonthlyChallenge model with fake data'

    def handle(self, *args, **kwargs):
        fake = Faker()
        months = [
            "Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
        ]

        # Clear existing data
        MonthlyChallenge.objects.all().delete()

        for month in months:
            challenge_text = fake.sentence(nb_words=10)
            MonthlyChallenge.objects.create(month=month, challenge_text=challenge_text)

        self.stdout.write(self.style.SUCCESS('Successfully populated the MonthlyChallenge model'))
