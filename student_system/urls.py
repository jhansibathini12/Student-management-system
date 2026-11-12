"""
Main URL Configuration for Student Management System.

The `urlpatterns` list routes URLs to views.
Includes:
- Django Admin interface
- Frontend Student Management views (Dashboard, CRUD, Auth)
- Django REST Framework API endpoints (/api/students/...)
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django Built-in Admin Panel
    path('admin/', admin.site.urls),

    # Frontend Web Application (Dashboard, Student CRUD, User Auth)
    path('', include('students.urls')),

    # REST API Endpoints
    path('api/', include('students.api_urls')),
]
