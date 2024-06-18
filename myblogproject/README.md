# Step 1: Set Up Your Django Project:
1. Install Django:

2. Create a New Django Project:
- django-admin startproject myblogproject
- cd myblogproject

3. Create a Blog Application:
- python manage.py startapp blog

4. Register the Blog App: Add 'blog' to the INSTALLED_APPS list in myblogproject/settings.py

/* myblogproject/settings.py */

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'blog',
    ]

# Step 2: Create the Blog Post Model
1. Define the Model:

/* blog/models.py */

    from django.db import models
    from django.utils import timezone

    class Post(models.Model):
        title = models.CharField(max_length=200)
        content = models.TextField()
        created_at = models.DateTimeField(default=timezone.now)

        def __str__(self):
            return self.title


2. Apply Migrations:
- python manage.py makemigrations
- python manage.py migrate

# Step 3: Create the Blog Post Views

1. Define Views for CRUD Operations:

/* blog/views.py */

    from django.shortcuts import render, get_object_or_404, redirect
    from .models import Post
    from .forms import PostForm

    def post_list(request):
        posts = Post.objects.all()
        return render(request, 'blog/post_list.html', {'posts': posts})

    def post_detail(request, pk):
        post = get_object_or_404(Post, pk=pk)
        return render(request, 'blog/post_detail.html', {'post': post})

    def post_new(request):
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.save()
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})

    def post_edit(request, pk):
        post = get_object_or_404(Post, pk=pk)
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.save()
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})

    def post_delete(request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return redirect('post_list')

2. Create a Form for the Blog Post:

/* blog/forms.py */

    from django import forms
    from .models import Post

    class PostForm(forms.ModelForm):
        class Meta:
            model = Post
            fields = ('title', 'content')

# Step 4: Create URLs for the Blog App

1. Define URLs:

/* blog/urls.py */
    from django.urls import path
    from . import views

    urlpatterns = [
        path('', views.post_list, name='post_list'),
        path('post/<int:pk>/', views.post_detail, name='post_detail'),
        path('post/new/', views.post_new, name='post_new'),
        path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
        path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    ]

2. Include Blog URLs in the Project:

/* myblogproject/urls.py */

    from django.contrib import admin
    from django.urls import path, include

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('blog.urls')),
    ]

# Step 5: Create Templates for the Blog

1. Create the templates Directory:
- mkdir blog/templates/blog

2. Create Template Files:

/* post_list.html: */

    <!-- blog/templates/blog/post_list.html -->
    <!DOCTYPE html>
    <html>
    <head>
        <title>Blog Posts</title>
    </head>
    <body>
        <h1>Blog Posts</h1>
        <a href="{% url 'post_new' %}">New Post</a>
        <ul>
            {% for post in posts %}
            <li>
                <a href="{% url 'post_detail' pk=post.pk %}">{{ post.title }}</a>
                <a href="{% url 'post_edit' pk=post.pk %}">Edit</a>
                <a href="{% url 'post_delete' pk=post.pk %}">Delete</a>
            </li>
            {% endfor %}
        </ul>
    </body>
    </html>

/* post_detail.html: */

    <!-- blog/templates/blog/post_detail.html -->
    <!DOCTYPE html>
    <html>
    <head>
        <title>{{ post.title }}</title>
    </head>
    <body>
        <h1>{{ post.title }}</h1>
        <p>{{ post.content }}</p>
        <a href="{% url 'post_edit' pk=post.pk %}">Edit</a>
        <a href="{% url 'post_delete' pk=post.pk %}">Delete</a>
        <a href="{% url 'post_list' %}">Back to list</a>
    </body>
    </html>

/* post_edit.html: */

    <!-- blog/templates/blog/post_edit.html -->
    <!DOCTYPE html>
    <html>
    <head>
        <title>New/Edit Post</title>
    </head>
    <body>
        <h1>New/Edit Post</h1>
        <form method="post">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit">Save</button>
        </form>
        <a href="{% url 'post_list' %}">Back to list</a>
    </body>
    </html>

# Step 6: Run the Server and Test

1. Run the Development Server:
- python manage.py runserver

2. Access the Blog Application:
- Open your browser and go to http://127.0.0.1:8000/
