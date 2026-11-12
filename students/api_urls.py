"""
API URL Routing for Student Management System.

Maps REST API endpoints to their corresponding API views.
"""

from django.urls import path
from . import api_views

app_name = 'students_api'

urlpatterns = [
    # List all students / Create new student
    path('students/', api_views.StudentListCreateAPIView.as_view(), name='student_list_create'),

    # Retrieve, Update (PUT/PATCH), Delete individual student by ID or student_id
    path('students/<str:identifier>/', api_views.StudentDetailAPIView.as_view(), name='student_detail_api'),
]
