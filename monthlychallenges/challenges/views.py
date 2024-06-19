# challenges/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import MonthlyChallenge
from .forms import MonthlyChallengeForm

def index(request):
    challenges = MonthlyChallenge.objects.all()
    return render(request, 'challenges/index.html', {'challenges': challenges})

def monthly_challenge(request, month):
    challenge = get_object_or_404(MonthlyChallenge, month=month)
    return render(request, 'challenges/challenge.html', {'challenge': challenge})

def add_challenge(request):
    if request.method == 'POST':
        form = MonthlyChallengeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = MonthlyChallengeForm()
    return render(request, 'challenges/add_challenge.html', {'form': form})