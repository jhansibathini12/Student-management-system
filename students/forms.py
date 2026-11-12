"""
Django forms for the Student Management System.

Contains:
- StudentForm: ModelForm for creating and updating student records with Bootstrap styling.
- UserRegistrationForm: Form for registering new admin/staff users.
- UserLoginForm: Form for authenticating existing users.
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from .models import Student
import re


class StudentForm(forms.ModelForm):
    """
    Form for adding and editing Student records.
    Renders with Bootstrap 5 input classes, custom placeholders, and field validations.
    """

    class Meta:
        model = Student
        fields = [
            'full_name',
            'email',
            'phone',
            'age',
            'gender',
            'course',
            'address',
            'date_of_joining',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter full name (e.g. John Doe)',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'name@example.com',
                'required': True,
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+1 (555) 000-0000',
                'required': True,
            }),
            'age': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 21',
                'min': '5',
                'max': '100',
                'required': True,
            }),
            'gender': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
            }),
            'course': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter residential address...',
                'required': True,
            }),
            'date_of_joining': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True,
            }),
        }

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None and (age < 5 or age > 100):
            raise ValidationError("Please enter a realistic age between 5 and 100.")
        return age

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        # Ensure phone has digits and reasonable length
        digits = re.sub(r'\D', '', phone)
        if len(digits) < 7 or len(digits) > 15:
            raise ValidationError("Please enter a valid phone number with 7 to 15 digits.")
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        # Verify uniqueness excluding the current instance if editing
        qs = Student.objects.filter(email__iexact=email)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("A student with this email address is already registered.")
        return email


class UserRegistrationForm(forms.ModelForm):
    """
    Create Admin Account form with Username, Email, Password, and Confirm Password.
    Removes First Name and Last Name.
    Accepts any user-chosen password without complexity restrictions,
    and securely hashes it before storing.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'name@example.com',
            'required': True,
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
            'required': True,
        })
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Re-enter your password',
            'required': True,
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter username',
                'required': True,
            }),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError("A user with this username already exists. Please choose a different one.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("A user with this email address already exists. Please choose a different one.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match. Please re-enter.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        # Securely hash the chosen password with PBKDF2 algorithm (never store in plain text)
        user.set_password(self.cleaned_data['password'])
        user.is_staff = True  # Ensure administrative access
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    """
    Customized login form styled with Bootstrap 5 classes.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter username',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password',
        })
