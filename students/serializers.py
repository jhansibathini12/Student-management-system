"""
Django REST Framework serializers for Student Management System.

Converts complex Student model instances to native Python datatypes
that can easily be rendered into JSON responses, and validates
incoming JSON payloads for creating and updating student records.
"""

from rest_framework import serializers
from .models import Student
import re


class StudentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Student model.
    Exposes all student details and validates business rules.
    """

    class Meta:
        model = Student
        fields = [
            'id',
            'student_id',
            'full_name',
            'email',
            'phone',
            'age',
            'gender',
            'course',
            'address',
            'date_of_joining',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'student_id', 'created_at', 'updated_at']

    def validate_age(self, value):
        """Validate that age is within acceptable bounds."""
        if value < 5 or value > 100:
            raise serializers.ValidationError("Age must be between 5 and 100.")
        return value

    def validate_phone(self, value):
        """Validate phone number length and format."""
        digits = re.sub(r'\D', '', value)
        if len(digits) < 7 or len(digits) > 15:
            raise serializers.ValidationError("Phone number must contain between 7 and 15 digits.")
        return value

    def validate_email(self, value):
        """Validate email uniqueness."""
        email = value.strip().lower()
        qs = Student.objects.filter(email__iexact=email)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("A student with this email already exists.")
        return email
