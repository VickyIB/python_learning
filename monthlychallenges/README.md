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