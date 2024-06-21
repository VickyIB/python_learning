from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UserRegisterForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def create_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        User.objects.create_user(username=username, email=email, password=password)
        return redirect('list_users')
    return render(request, 'accounts/create_user.html')

def list_users(request):
    users = User.objects.all()
    return render(request, 'accounts/list_users.html', {'users': users})

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')