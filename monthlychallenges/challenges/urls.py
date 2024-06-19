# challenges/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:month>/', views.monthly_challenge, name='monthly_challenge'),
]