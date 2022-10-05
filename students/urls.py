from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('course/', views.course, name='course'),
    path('register/', views.register, name='register'),
    path('about/',views.runoob),
    path('recommendation/', views.recommendation, name='recommendation'),
]