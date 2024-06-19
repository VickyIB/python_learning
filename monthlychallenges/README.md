# Step 1: Set Up Your Django Project

1. Create a New Django Project:
- django-admin startproject monthlychallenges
- cd monthlychallenges

2. Create the Challenges Application:
- python manage.py startapp challenges

3. Register the Challenges App: Add 'challenges' to the INSTALLED_APPS list in monthlychallenges/settings.py

        /* monthlychallenges/settings.py */
        INSTALLED_APPS = [
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'challenges',
        ]

# Step 2: Create Models for Monthly Challenges

1. Define the Model:

        /* challenges/models.py */
        from django.db import models

        class MonthlyChallenge(models.Model):
            month = models.CharField(max_length=20, unique=True)
            challenge_text = models.TextField()

            def __str__(self):
                return self.month.capitalize()

2. Apply Migrations:
- python manage.py makemigrations
- python manage.py migrate

# Step 3: Create Views for Monthly Challenges

1. Define Views:

        /* challenges/views.py */
        from django.shortcuts import render, get_object_or_404
        from .models import MonthlyChallenge

        def index(request):
            challenges = MonthlyChallenge.objects.all()
            return render(request, 'challenges/index.html', {'challenges': challenges})

        def monthly_challenge(request, month):
            challenge = get_object_or_404(MonthlyChallenge, month=month)
            return render(request, 'challenges/challenge.html', {'challenge': challenge})

# Step 4: Create URLs for the Challenges App

1. Define URLs:

        /* challenges/urls.py */
        from django.urls import path
        from . import views

        urlpatterns = [
            path('', views.index, name='index'),
            path('<str:month>/', views.monthly_challenge, name='monthly_challenge'),
        ]

2. Include Challenges URLs in the Project:

        /* monthlychallenges/urls.py */
        from django.contrib import admin
        from django.urls import path, include

        urlpatterns = [
            path('admin/', admin.site.urls),
            path('', include('challenges.urls')),
        ]

# Step 5: Create a Custom Template Filter

1. Create a new Python file for the custom filter:

Create a file named templatetags directory inside your challenges app if it doesn't exist already:
- mkdir -p challenges/templatetags

Inside the templatetags directory, create a file named challenges_filters.py:
touch challenges/templatetags/challenges_filters.py

2. Define the Custom Filter:

        /* challenges/templatetags/challenges_filters.py */
        from django import template

        register = template.Library()

        @register.filter(name='capitalize')
        def capitalize(value):
            return value.capitalize()

3. Create an __init__.py File:

To make the templatetags directory a package, create an __init__.py file:
- touch challenges/templatetags/__init__.py

# Step 6: Create Templates for Monthly Challenges

1. Create the templates Directory:
- mkdir -p challenges/templates/challenges

2. Create Template Files:
- index.html

        <!-- challenges/templates/challenges/index.html -->
        <!DOCTYPE html>
        <html>
        <head>
            <title>Monthly Challenges</title>
            {% load static %}
            {% load challenges_filters %}
            <link rel="stylesheet" type="text/css" href="{% static 'challenges/styles.css' %}">
        </head>
        <body>
            <h1>Monthly Challenges</h1>
            <ul>
                {% for challenge in challenges %}
                <li>
                    <a href="{% url 'monthly_challenge' month=challenge.month %}">{{ challenge.month|capitalize }}</a>
                </li>
                {% endfor %}
            </ul>
        </body>
        </html>

- challenge.html

        <!-- challenges/templates/challenges/challenge.html -->
        <!DOCTYPE html>
        <html>
        <head>
            {% load static %}
            {% load challenges_filters %}
            <title>{{ challenge.month|capitalize }} Challenge</title>
            <link rel="stylesheet" type="text/css" href="{% static 'challenges/styles.css' %}">
        </head>
        <body>
            <h1>{{ challenge.month|capitalize }} Challenge</h1>
            <p>{{ challenge.challenge_text }}</p>
            <a href="{% url 'index' %}">Back to all challenges</a>
        </body>
        </html>

# Step 7: Add Static Files

1. Create the static Directory:
- mkdir -p challenges/static/challenges

2. Create a CSS File:
- styles.css:

        /* challenges/static/challenges/styles.css */
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
        }
        h1 {
            background-color: #333;
            color: #fff;
            padding: 10px;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        li {
            background-color: #fff;
            margin: 10px;
            padding: 10px;
            border: 1px solid #ddd;
        }
        a {
            text-decoration: none;
            color: #333;
        }
        a:hover {
            color: #007bff;
        }

3. Update settings.py to Configure Static Files:

        /* monthlychallenges/settings.py */
        import os

        STATIC_URL = '/static/'
        STATICFILES_DIRS = [
            os.path.join(BASE_DIR, 'challenges/static'),
        ]

# Step 8: Using the Django Admin Interface

1. Create a Superuser:

If you haven't created a superuser yet, you can create one using the following command:
- python manage.py createsuperuser

2. Register the Model in the Admin Interface:

Open the challenges/admin.py file and register the MonthlyChallenge model:

        /* challenges/admin.py */
        from django.contrib import admin
        from .models import MonthlyChallenge

        admin.site.register(MonthlyChallenge)

# Step 9: Run the Server and Test

1. Run the Development Server:
- python manage.py runserver

2. Access the Application: 
- Open your browser and go to http://127.0.0.1:8000/ to see the list of monthly challenges with the applied CSS styles.

3. Access the Admin Interface:
- Open your browser and go to http://127.0.0.1:8000/admin/. Log in with the superuser credentials you created.

4. Add Monthly Challenges:
- In the admin interface, click on "Monthly Challenges".
- Click "Add Monthly Challenge" to add new challenges.
- Fill in the month and challenge_text fields.
- Save the changes.

# Step 10:  Install the Faker Library

Faker is a Python package that generates fake data for you.
- conda install faker / pip install faker

# Step 11: Create a Management Command to Populate the Database

1. Create the Management Command Directory:

Create a directory for custom management commands within the challenges app:
- mkdir -p challenges/management/commands

2. Create an Empty __init__.py File:

Create empty __init__.py files to ensure Python treats these directories as packages:
- touch challenges/management/__init__.py
- touch challenges/management/commands/__init__.py

3. Create the Management Command Script:

Create a script named populate_challenges.py within the commands directory:
- touch challenges/management/commands/populate_challenges.py

4. Write the Population Script:

Open populate_challenges.py and write the following code:

        /* challenges/management/commands/populate_challenges.py */
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

# Step 12: Run the Population Script

Run the custom management command to populate the database with fake data:
- python manage.py populate_challenges

# Step 13: Verifying the Data
- After running the script, you can verify the data by running the server and navigating to http://127.0.0.1:8000/ or checking the Django admin interface.

# Step 14: Create the Model Form

1. Create the Forms File:

Create a file named forms.py within the challenges app:
- touch challenges/forms.py

2. Define the Model Form:

Open forms.py and write the following code:

        /* challenges/forms.py */
        from django import forms
        from .models import MonthlyChallenge

        class MonthlyChallengeForm(forms.ModelForm):
            class Meta:
                model = MonthlyChallenge
                fields = ['month', 'challenge_text']

            def clean_month(self):
                month = self.cleaned_data.get('month')
                if not month.isalpha():
                    raise forms.ValidationError('Month name should contain only letters.')
                return month.lower()

# Step 15: Update the View to Handle the Form

Open views.py and write the following code to handle form rendering and submission:

        /* challenges/views.py */
        from django.shortcuts import render, redirect
        from .forms import MonthlyChallengeForm

        def add_challenge(request):
            if request.method == 'POST':
                form = MonthlyChallengeForm(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect('index')
            else:
                form = MonthlyChallengeForm()
            return render(request, 'challenges/add_challenge.html', {'form': form})

# Step 16: Update URLs for the Form View

1. Define URLs:

Open urls.py and add a path for the new view:

        /* challenges/urls.py */
        from django.urls import path
        from . import views

        urlpatterns = [
            path('', views.index, name='index'),
            path('add/', views.add_challenge, name='add_challenge'),
            path('<str:month>/', views.monthly_challenge, name='monthly_challenge'),
        ]

# Step 17: Create the Template for the Form

1. Create the Template File:

Create a file named add_challenge.html within the templates/challenges directory:
- touch challenges/templates/challenges/add_challenge.html

2. Write the Template:

Open add_challenge.html and write the following code:

        <!-- challenges/templates/challenges/add_challenge.html -->
        <!DOCTYPE html>
        <html>
        <head>
            <title>Add Monthly Challenge</title>
            {% load static %}
            <link rel="stylesheet" type="text/css" href="{% static 'challenges/styles.css' %}">
        </head>
        <body>
            <h1>Add Monthly Challenge</h1>
            <form method="post">
                {% csrf_token %}
                {{ form.as_p }}
                <button type="submit">Add Challenge</button>
            </form>
            <a href="{% url 'index' %}">Back to all challenges</a>
        </body>
        </html>

# Step 18: Run the Server and Test

1. Run the Development Server:
- python manage.py runserver

2. Access the Application: 
- Open your browser and go to http://127.0.0.1:8000/add/ to access the form for adding new monthly challenges. Fill in the form and submit to test the validation and saving functionality.