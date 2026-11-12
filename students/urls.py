"""
Frontend URL Configuration for the Students App.

Connects web browser routes to their respective views:
- Dashboard
- Student CRUD operations
- User Authentication (Login, Register, Logout)
"""

from django.urls import path
from . import views

urlpatterns = [
    # Dashboard (Home view)
    path('', views.dashboard, name='dashboard'),

    # Student Management
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.student_create, name='student_create'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
    path('students/<int:pk>/edit/', views.student_update, name='student_update'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),

    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
]
