# creating a login registration, logout functionality and explore the User model and Django passwords

Creating login, registration, and logout functionality in Django involves setting up views, forms, templates, and configuring the necessary URLs. Additionally, Django’s built-in User model and authentication system provide a robust framework for handling user accounts and passwords securely. Below is a step-by-step guide to setting up these features.

## Step 1: Create a Django app:
- python manage.py startapp accounts

- Add the app to INSTALLED_APPS in myproject/settings.py:

        INSTALLED_APPS = [
            ...
            'accounts',
        ]

## Creating User Registration

1. Create a registration form:

In accounts/forms.py:

        from django.core.exceptions import ValidationError
        from django import forms
        from django.contrib.auth.models import User
        from django.contrib.auth.forms import UserCreationForm

        class UserRegisterForm(UserCreationForm):
            email = forms.EmailField()

            class Meta:
                model = User
                fields = ['username', 'email', 'password1', 'password2']
                
            def clean_password2(self):
                password1 = self.cleaned_data.get('password1')
                password2 = self.cleaned_data.get('password2')
                if password1 and password2 and password1 != password2:
                    raise ValidationError("Passwords don't match")
                return password2

2. Create the registration view:

In accounts/views.py:

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

## Step 3: Setting Up Login and Logout

1. Configure URLs:

- In accounts/urls.py:

        from django.urls import path
        from django.contrib.auth import views as auth_views
        from . import views

        urlpatterns = [
            path('register/', views.register, name='register'),
            path('create/', views.create_user, name='create_user'),
            path('users/', views.list_users, name='list_users'),
            path('accounts/login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
            path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
            path('accounts/profile/', views.profile, name='profile'),
        ]

- In monthlychallenges/urls.py:

        urlpatterns = [
            path('admin/', admin.site.urls),
            path('', include('challenges.urls')),
            path('', include('accounts.urls')),
        ]

2. Create login template:

In accounts/templates/accounts/login.html:

        <!DOCTYPE html>
        <html>
        <head>
            <title>Login</title>
        </head>
        <body>
            <h2>Login</h2>
            <form method="post">
                {% csrf_token %}
                {{ form.as_p }}
                <button type="submit">Login</button>
            </form>
        </body>
        </html>

3. Create logout template:

In accounts/templates/accounts/logout.html:

        <!DOCTYPE html>
        <html>
        <head>
            <title>Logout</title>
        </head>
        <body>
            <h2>Logged Out</h2>
            <p>You have been logged out.</p>
            <a href="{% url 'login' %}">Login again</a>
        </body>
        </html>

3. Create register template:

In accounts/templates/accounts/register.html:

        <!DOCTYPE html>
        <html>
        <head>
            <title>Register</title>
        </head>
        <body>
            <h2>Register</h2>
            <form method="post">
                {% csrf_token %}
                {{ form.as_p }}
                <button type="submit">Register</button>
            </form>
        </body>
        </html>

4. Create create_user template:

In accounts/templates/accounts/create_user.html

        <!DOCTYPE html>
        <html>
        <head>
            <title>Create User</title>
        </head>
        <body>
            <h2>Create User</h2>
            <form method="post">
                {% csrf_token %}
                <label for="username">Username:</label>
                <input type="text" id="username" name="username" required><br><br>
                <label for="email">Email:</label>
                <input type="email" id="email" name="email" required><br><br>
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required><br><br>
                <button type="submit">Create</button>
            </form>
        </body>
        </html>

5. Create list_users template:

- In accounts/templates/accounts/list_users.html

        <!DOCTYPE html>
        <html>
        <head>
            <title>List Users</title>
        </head>
        <body>
            <h2>Users List</h2>
            <ul>
                {% for user in users %}
                    <li>{{ user.username }} ({{ user.email }})</li>
                {% endfor %}
            </ul>
            <a href="{% url 'profile' %}">User Profile</a> | <a href="{% url 'create_user' %}">Create a new user</a> | <a href="{% url 'logout' %}">Logout</a>
        </body>
        </html>

6. Create profile template:

- In accounts/templates/accounts/profile.html

        <!DOCTYPE html>
        <html>
        <head>
            <title>Profile</title>
        </head>
        <body>
            <h2>Welcome, {{ user.username }}!</h2>
            <p>Email: {{ user.email }}</p>
            <a href="{% url 'list_users' %}">User List</a> | <a href="{% url 'logout' %}">Logout</a>
        </body>
        </html>

## Step 4: Configuring Django Passwords

1. Set password validation in myproject/settings.py:

        AUTH_PASSWORD_VALIDATORS = [
            {
                'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
            },
            {
                'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
            },
            {
                'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
            },
            {
                'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
            },
        ]

2. Optional: Customizing Password Validation Messages:

        from django.core.exceptions import ValidationError
        from django import forms
        from django.contrib.auth.models import User
        from django.contrib.auth.forms import UserCreationForm

        class UserRegisterForm(UserCreationForm):
            email = forms.EmailField()

            class Meta:
                model = User
                fields = ['username', 'email', 'password1', 'password2']
                
            def clean_password2(self):
                password1 = self.cleaned_data.get('password1')
                password2 = self.cleaned_data.get('password2')
                if password1 and password2 and password1 != password2:
                    raise ValidationError("Passwords don't match")
                return password2

## Step 5: Running the Project

1. Apply Migrations:
- python manage.py migrate

2. Run the Development Server:
- python manage.py runserver

3. Access the URLs:
- Register a new user: http://127.0.0.1:8000/register/
- Create a user manually: http://127.0.0.1:8000/create/
- List users: http://127.0.0.1:8000/users/