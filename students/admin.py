"""
Django Admin configuration for the Student model.

Enables administrators to view, search, filter, and edit student records
through the built-in Django Admin interface.
"""

from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """
    Custom Admin interface configuration for Student model.
    """
    list_display = (
        'student_id',
        'full_name',
        'email',
        'phone',
        'course',
        'age',
        'gender',
        'date_of_joining',
    )
    list_filter = ('course', 'gender', 'date_of_joining')
    search_fields = ('student_id', 'full_name', 'email', 'phone', 'course')
    readonly_fields = ('student_id', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    list_per_page = 20

    fieldsets = (
        ('Identification', {
            'fields': ('student_id', 'full_name', 'email', 'phone')
        }),
        ('Academic & Demographics', {
            'fields': ('course', 'age', 'gender', 'date_of_joining')
        }),
        ('Residential Details', {
            'fields': ('address',)
        }),
        ('System Timestamps', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at')
        }),
    )
