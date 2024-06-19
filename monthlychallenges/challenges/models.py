# challenges/models.py
from django.db import models

class MonthlyChallenge(models.Model):
    month = models.CharField(max_length=20, unique=True)
    challenge_text = models.TextField()

    def __str__(self):
        return self.month.capitalize()