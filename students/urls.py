from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('recommendation/', views.recommendation, name='recommendation'),
    path('home/', views.home, name='home'),
    path('', views.index, name='index'),
]