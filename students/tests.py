"""
Automated tests for Student Management System.

Tests:
1. Model tests (auto student_id generation, string representation, uniqueness)
2. Frontend views tests (Dashboard, Student List, Create, Update, Delete, Auth protection)
3. REST API tests (GET, POST, PUT, PATCH, DELETE, Search, Filter, Validation)
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from students.models import Student
from datetime import date
import json


class StudentModelAndViewsTestCase(TestCase):
    def setUp(self):
        # Create staff user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
            email='testuser@example.com'
        )
        self.client = Client()

        # Create sample students
        self.student1 = Student.objects.create(
            full_name="Alice Johnson",
            email="alice@example.com",
            phone="+1 (555) 111-2222",
            age=21,
            gender="Female",
            course="Computer Science",
            address="123 Tech Lane",
            date_of_joining=date(2025, 9, 1)
        )
        self.student2 = Student.objects.create(
            full_name="Bob Smith",
            email="bob@example.com",
            phone="+1 (555) 333-4444",
            age=23,
            gender="Male",
            course="Data Science",
            address="456 Innovation Blvd",
            date_of_joining=date(2025, 9, 15)
        )

    def test_student_auto_id_generation(self):
        """Verify student_id is automatically generated in format STU0001, etc."""
        self.assertTrue(self.student1.student_id.startswith("STU"))
        self.assertTrue(self.student2.student_id.startswith("STU"))
        self.assertNotEqual(self.student1.student_id, self.student2.student_id)

    def test_unauthenticated_user_redirected(self):
        """Unauthenticated requests must be redirected to login page."""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_dashboard_authenticated(self):
        """Dashboard renders successfully for logged in user."""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alice Johnson")
        self.assertContains(response, "Total Students")

    def test_student_list_search_and_filter(self):
        """Test student directory search and course filtering."""
        self.client.login(username='testuser', password='testpassword123')

        # Full list
        response = self.client.get(reverse('student_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alice Johnson")
        self.assertContains(response, "Bob Smith")

        # Search by name
        response_search = self.client.get(reverse('student_list'), {'q': 'Alice'})
        self.assertContains(response_search, "Alice Johnson")
        self.assertNotContains(response_search, "Bob Smith")

        # Filter by course
        response_filter = self.client.get(reverse('student_list'), {'course': 'Data Science'})
        self.assertContains(response_filter, "Bob Smith")
        self.assertNotContains(response_filter, "Alice Johnson")

    def test_student_create_view(self):
        """Test adding a new student via HTML form."""
        self.client.login(username='testuser', password='testpassword123')
        post_data = {
            'full_name': 'Charlie Brown',
            'email': 'charlie@example.com',
            'phone': '+1 (555) 555-6666',
            'age': 20,
            'gender': 'Male',
            'course': 'Cybersecurity',
            'address': '789 Secure Way',
            'date_of_joining': '2026-01-15'
        }
        response = self.client.post(reverse('student_create'), post_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Student.objects.filter(email='charlie@example.com').exists())

    def test_student_update_view(self):
        """Test updating student details."""
        self.client.login(username='testuser', password='testpassword123')
        update_data = {
            'full_name': 'Alice Johnson Updated',
            'email': 'alice@example.com',
            'phone': '+1 (555) 111-9999',
            'age': 22,
            'gender': 'Female',
            'course': 'Computer Science',
            'address': 'New Updated Address',
            'date_of_joining': '2025-09-01'
        }
        response = self.client.post(reverse('student_update', kwargs={'pk': self.student1.pk}), update_data)
        self.assertEqual(response.status_code, 302)
        self.student1.refresh_from_db()
        self.assertEqual(self.student1.full_name, 'Alice Johnson Updated')
        self.assertEqual(self.student1.age, 22)

    def test_student_delete_view(self):
        """Test deleting student record."""
        self.client.login(username='testuser', password='testpassword123')
        student_id_to_delete = self.student2.pk
        response = self.client.post(reverse('student_delete', kwargs={'pk': student_id_to_delete}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Student.objects.filter(pk=student_id_to_delete).exists())

    def test_register_admin_account_any_password(self):
        """Test creating an account with any password without complexity requirements."""
        reg_data = {
            'username': 'newadmin',
            'email': 'newadmin@example.com',
            'password': '123',
            'confirm_password': '123'
        }
        response = self.client.post(reverse('register'), reg_data)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

        # Check user is created in database, has staff access, and password is encrypted
        user = User.objects.get(username='newadmin')
        self.assertTrue(user.is_staff)
        self.assertTrue(user.password.startswith('pbkdf2_sha256$'))
        self.assertNotEqual(user.password, '123')

        # Verify user can log in with that exact password
        login_res = self.client.post(reverse('login'), {'username': 'newadmin', 'password': '123'})
        self.assertEqual(login_res.status_code, 302)
        self.assertIn(reverse('dashboard'), login_res.url)

    def test_register_admin_account_password_mismatch(self):
        """Test registration fails with a clean error when passwords do not match."""
        mismatch_data = {
            'username': 'mismatchuser',
            'email': 'mismatch@example.com',
            'password': 'password1',
            'confirm_password': 'password2'
        }
        response = self.client.post(reverse('register'), mismatch_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Passwords do not match. Please re-enter.")
        self.assertFalse(User.objects.filter(username='mismatchuser').exists())


class StudentAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.student = Student.objects.create(
            full_name="Diana Prince",
            email="diana@example.com",
            phone="+1 (555) 777-8888",
            age=22,
            gender="Female",
            course="Artificial Intelligence",
            address="Paradise Island Way",
            date_of_joining=date(2025, 8, 1)
        )

    def test_api_list_students(self):
        """Test GET /api/students/"""
        response = self.client.get('/api/students/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertGreaterEqual(data['count'], 1)
        self.assertEqual(data['data'][0]['full_name'], 'Diana Prince')

    def test_api_create_student(self):
        """Test POST /api/students/ with valid JSON payload."""
        payload = {
            "full_name": "Bruce Wayne",
            "email": "bruce@example.com",
            "phone": "+1 (555) 999-0000",
            "age": 24,
            "gender": "Male",
            "course": "Cybersecurity",
            "address": "1007 Mountain Drive, Gotham",
            "date_of_joining": "2026-02-10"
        }
        response = self.client.post(
            '/api/students/',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        res_data = response.json()
        self.assertEqual(res_data['status'], 'success')
        self.assertEqual(res_data['data']['full_name'], 'Bruce Wayne')
        self.assertTrue(res_data['data']['student_id'].startswith('STU'))

    def test_api_create_student_validation_error(self):
        """Test POST /api/students/ with invalid email and age."""
        invalid_payload = {
            "full_name": "Invalid Student",
            "email": "not-an-email",
            "phone": "123",  # Too short
            "age": 150,      # Unrealistic age (>100)
            "gender": "Male",
            "course": "Computer Science",
            "address": "Test Address",
            "date_of_joining": "2026-01-01"
        }
        response = self.client.post(
            '/api/students/',
            data=json.dumps(invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        res_data = response.json()
        self.assertEqual(res_data['status'], 'error')
        self.assertIn('email', res_data['errors'])
        self.assertIn('age', res_data['errors'])

    def test_api_get_student_by_pk_and_code(self):
        """Test GET /api/students/<id>/ via numeric PK and string student_id."""
        # By numeric primary key
        res_pk = self.client.get(f'/api/students/{self.student.pk}/')
        self.assertEqual(res_pk.status_code, 200)
        self.assertEqual(res_pk.json()['data']['full_name'], 'Diana Prince')

        # By alphanumeric student_id (e.g. STU0001)
        res_code = self.client.get(f'/api/students/{self.student.student_id}/')
        self.assertEqual(res_code.status_code, 200)
        self.assertEqual(res_code.json()['data']['student_id'], self.student.student_id)

    def test_api_put_student(self):
        """Test PUT /api/students/<id>/ for full update."""
        update_payload = {
            "full_name": "Diana Prince Updated",
            "email": "diana.new@example.com",
            "phone": "+1 (555) 777-9999",
            "age": 23,
            "gender": "Female",
            "course": "Artificial Intelligence",
            "address": "New Paradise Road",
            "date_of_joining": "2025-08-01"
        }
        response = self.client.put(
            f'/api/students/{self.student.pk}/',
            data=json.dumps(update_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data']['full_name'], 'Diana Prince Updated')

    def test_api_patch_student(self):
        """Test PATCH /api/students/<id>/ for partial update."""
        patch_payload = {
            "phone": "+1 (555) 000-1111"
        }
        response = self.client.patch(
            f'/api/students/{self.student.pk}/',
            data=json.dumps(patch_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data']['phone'], '+1 (555) 000-1111')

    def test_api_delete_student(self):
        """Test DELETE /api/students/<id>/"""
        response = self.client.delete(f'/api/students/{self.student.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertFalse(Student.objects.filter(pk=self.student.pk).exists())
