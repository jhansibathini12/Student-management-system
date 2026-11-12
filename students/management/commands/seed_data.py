"""
Management command to seed the database with initial sample students and a superuser.

Usage:
    python manage.py seed_data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from students.models import Student
from datetime import date


class Command(BaseCommand):
    help = "Seeds initial students and superuser admin account"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Initializing seed process..."))

        # 1. Create or get Superuser
        admin_username = "admin"
        admin_email = "admin@example.com"
        admin_password = "admin123"

        if not User.objects.filter(username=admin_username).exists():
            User.objects.create_superuser(
                username=admin_username,
                email=admin_email,
                password=admin_password,
                first_name="System",
                last_name="Administrator"
            )
            self.stdout.write(self.style.SUCCESS(
                f"Created superuser: '{admin_username}' with password: '{admin_password}'"
            ))
        else:
            self.stdout.write(self.style.WARNING(f"Superuser '{admin_username}' already exists."))

        # 2. Sample Students Dataset
        sample_students = [
            {
                "full_name": "Aarav Sharma",
                "email": "aarav.sharma@example.com",
                "phone": "+1 (555) 234-5678",
                "age": 20,
                "gender": "Male",
                "course": "Computer Science",
                "address": "402 Tech Park Boulevard, Austin, TX",
                "date_of_joining": date(2025, 8, 15),
            },
            {
                "full_name": "Sophia Martinez",
                "email": "sophia.m@example.com",
                "phone": "+1 (555) 345-6789",
                "age": 21,
                "gender": "Female",
                "course": "Data Science",
                "address": "78 Silicon Hill Way, San Jose, CA",
                "date_of_joining": date(2025, 9, 1),
            },
            {
                "full_name": "Liam Johnson",
                "email": "liam.johnson@example.com",
                "phone": "+1 (555) 456-7890",
                "age": 22,
                "gender": "Male",
                "course": "Artificial Intelligence",
                "address": "12 Innovation Drive, Boston, MA",
                "date_of_joining": date(2025, 7, 20),
            },
            {
                "full_name": "Emily Chen",
                "email": "emily.chen@example.com",
                "phone": "+1 (555) 567-8901",
                "age": 19,
                "gender": "Female",
                "course": "Information Technology",
                "address": "904 University Avenue, Seattle, WA",
                "date_of_joining": date(2026, 1, 10),
            },
            {
                "full_name": "Marcus Williams",
                "email": "marcus.w@example.com",
                "phone": "+1 (555) 678-9012",
                "age": 23,
                "gender": "Male",
                "course": "Mechanical Engineering",
                "address": "55 Industry Parkway, Chicago, IL",
                "date_of_joining": date(2025, 6, 5),
            },
            {
                "full_name": "Olivia Taylor",
                "email": "olivia.taylor@example.com",
                "phone": "+1 (555) 789-0123",
                "age": 20,
                "gender": "Female",
                "course": "Cybersecurity",
                "address": "330 Cyber Avenue, Denver, CO",
                "date_of_joining": date(2025, 10, 12),
            },
            {
                "full_name": "David Kim",
                "email": "david.kim@example.com",
                "phone": "+1 (555) 890-1234",
                "age": 22,
                "gender": "Male",
                "course": "Business Administration",
                "address": "88 Wall Street Lane, New York, NY",
                "date_of_joining": date(2025, 8, 25),
            },
            {
                "full_name": "Ananya Patel",
                "email": "ananya.patel@example.com",
                "phone": "+1 (555) 901-2345",
                "age": 21,
                "gender": "Female",
                "course": "Computer Science",
                "address": "210 College Park Drive, Raleigh, NC",
                "date_of_joining": date(2025, 9, 15),
            },
            {
                "full_name": "Ethan Wright",
                "email": "ethan.wright@example.com",
                "phone": "+1 (555) 012-3456",
                "age": 20,
                "gender": "Male",
                "course": "Electrical Engineering",
                "address": "67 Voltage Road, Atlanta, GA",
                "date_of_joining": date(2026, 2, 1),
            },
            {
                "full_name": "Zoe Kravitz",
                "email": "zoe.kravitz@example.com",
                "phone": "+1 (555) 123-9876",
                "age": 22,
                "gender": "Other",
                "course": "Data Science",
                "address": "15 Heritage Grove, Portland, OR",
                "date_of_joining": date(2025, 11, 4),
            },
        ]

        created_count = 0
        for student_data in sample_students:
            if not Student.objects.filter(email=student_data["email"]).exists():
                Student.objects.create(**student_data)
                created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Successfully seeded {created_count} sample students into the database!"
        ))
