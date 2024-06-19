# challenges/views.py
from django.shortcuts import render, get_object_or_404
from .models import MonthlyChallenge

def index(request):
    challenges = MonthlyChallenge.objects.all()
    return render(request, 'challenges/index.html', {'challenges': challenges})

def monthly_challenge(request, month):
    challenge = get_object_or_404(MonthlyChallenge, month=month)
    return render(request, 'challenges/challenge.html', {'challenge': challenge})