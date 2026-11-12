"""
Models for the Student Management System.

Defines the Student model which stores all student records,
auto-generates unique student IDs, and defines choice fields.
"""

from django.db import models
from django.utils import timezone


class Student(models.Model):
    """
    Student model representing individual student profile records.
    
    Fields:
        student_id: Automatically generated unique identifier (e.g., STU0001).
        full_name: Student's complete legal name.
        email: Unique personal/institutional email address.
        phone: Contact phone number.
        age: Age in years (positive integer).
        gender: Gender selection (Male, Female, Other).
        course: Enrolled academic program/course.
        address: Residential/mailing address.
        date_of_joining: Date the student enrolled in the institution.
        created_at: Timestamp when record was created.
        updated_at: Timestamp when record was last modified.
    """

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    COURSE_CHOICES = [
        ('Computer Science', 'Computer Science'),
        ('Information Technology', 'Information Technology'),
        ('Data Science', 'Data Science'),
        ('Artificial Intelligence', 'Artificial Intelligence'),
        ('Mechanical Engineering', 'Mechanical Engineering'),
        ('Electrical Engineering', 'Electrical Engineering'),
        ('Civil Engineering', 'Civil Engineering'),
        ('Business Administration', 'Business Administration'),
        ('Cybersecurity', 'Cybersecurity'),
    ]

    # Automatically generated student identifier
    student_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        help_text="Automatically generated student ID (e.g., STU0001)"
    )

    full_name = models.CharField(
        max_length=120,
        verbose_name="Full Name",
        help_text="Enter student's full name"
    )

    email = models.EmailField(
        unique=True,
        verbose_name="Email Address",
        help_text="Valid and unique email address"
    )

    phone = models.CharField(
        max_length=20,
        verbose_name="Phone Number",
        help_text="Contact telephone number"
    )

    age = models.PositiveIntegerField(
        verbose_name="Age",
        help_text="Age in years (e.g., 20)"
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        default='Male',
        verbose_name="Gender"
    )

    course = models.CharField(
        max_length=60,
        choices=COURSE_CHOICES,
        default='Computer Science',
        verbose_name="Course"
    )

    address = models.TextField(
        verbose_name="Address",
        help_text="Residential or mailing address"
    )

    date_of_joining = models.DateField(
        default=timezone.now,
        verbose_name="Date of Joining",
        help_text="Enrollment date"
    )

    # Auditing timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return f"{self.student_id} - {self.full_name} ({self.course})"

    def save(self, *args, **kwargs):
        """
        Custom save method to auto-generate a sequential student_id if not present.
        Example: STU0001, STU0002, etc.
        """
        if not self.student_id:
            # Query the highest existing numerical ID or fallback
            last_student = Student.objects.all().order_by('id').last()
            next_num = (last_student.id + 1) if last_student else 1
            candidate = f"STU{next_num:04d}"

            # Ensure candidate is completely unique
            while Student.objects.filter(student_id=candidate).exists():
                next_num += 1
                candidate = f"STU{next_num:04d}"

            self.student_id = candidate

        super().save(*args, **kwargs)
