"""
Views for the Student Management System.

Handles:
- User Authentication (Login, Register, Logout)
- Dashboard with summary analytics and recent students
- Student CRUD operations (List, Detail, Create, Update, Delete)
- Search and course filtering
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count

from .models import Student
from .forms import StudentForm, UserRegistrationForm, UserLoginForm


# ==============================================================================
# Authentication Views
# ==============================================================================

def register_view(request):
    """Handle new user registration."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request,
                f"Admin account successfully created for '{user.username}'! You can now log in with your credentials."
            )
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors in the registration form below.")
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    """Handle user authentication and login."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            username = request.POST.get('username', '').strip()
            from django.contrib.auth.models import User
            if username and not User.objects.filter(username=username).exists():
                messages.error(
                    request,
                    f"No account found with username '{username}'. Please create an account first before logging in."
                )
            else:
                messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = UserLoginForm()

    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    """Handle user logout."""
    logout(request)
    messages.info(request, "You have been safely logged out. See you soon!")
    return redirect('login')


# ==============================================================================
# Dashboard & Analytics
# ==============================================================================

@login_required
def dashboard(request):
    """
    Main dashboard displaying key metrics, recent student enrollments,
    course distribution, and a quick-action student table.
    """
    total_students = Student.objects.count()

    # Distinct courses currently enrolled
    enrolled_courses = Student.objects.values('course').distinct().count()
    total_courses = max(enrolled_courses, len(Student.COURSE_CHOICES))

    # Gender breakdown
    male_count = Student.objects.filter(gender='Male').count()
    female_count = Student.objects.filter(gender='Female').count()
    other_gender_count = Student.objects.filter(gender='Other').count()

    # Course breakdown for summary cards/progress
    course_stats = (
        Student.objects.values('course')
        .annotate(total=Count('id'))
        .order_by('-total')[:5]
    )

    # 5 most recently added students
    recent_students = Student.objects.all().order_by('-created_at')[:5]

    # Latest 10 students for the interactive table on the dashboard
    dashboard_students = Student.objects.all().order_by('-created_at')[:10]

    context = {
        'total_students': total_students,
        'total_courses': total_courses,
        'male_count': male_count,
        'female_count': female_count,
        'other_gender_count': other_gender_count,
        'course_stats': course_stats,
        'recent_students': recent_students,
        'dashboard_students': dashboard_students,
    }
    return render(request, 'students/dashboard.html', context)


# ==============================================================================
# Student CRUD Operations
# ==============================================================================

@login_required
def student_list(request):
    """
    Display all student records in a table with search and filtering.
    Supports search by name, email, or course, and filter by course.
    """
    students = Student.objects.all()

    # Search functionality
    query = request.GET.get('q', '').strip()
    if query:
        students = students.filter(
            Q(full_name__icontains=query) |
            Q(email__icontains=query) |
            Q(course__icontains=query) |
            Q(student_id__icontains=query)
        )

    # Course filter functionality
    course_filter = request.GET.get('course', '').strip()
    if course_filter:
        students = students.filter(course=course_filter)

    # Pagination: 10 students per page
    paginator = Paginator(students, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    courses = [choice[0] for choice in Student.COURSE_CHOICES]

    context = {
        'page_obj': page_obj,
        'students': page_obj.object_list,
        'total_count': students.count(),
        'query': query,
        'course_filter': course_filter,
        'courses': courses,
    }
    return render(request, 'students/student_list.html', context)


@login_required
def student_detail(request, pk):
    """Display individual student profile and detailed records."""
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'students/student_detail.html', {'student': student})


@login_required
def student_create(request):
    """Render and process the Add Student form."""
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            messages.success(
                request,
                f"Student '{student.full_name}' was successfully added with ID {student.student_id}!"
            )
            return redirect('student_detail', pk=student.pk)
        else:
            messages.error(request, "Failed to create student. Please check the form errors below.")
    else:
        form = StudentForm()

    return render(request, 'students/student_form.html', {
        'form': form,
        'title': 'Add New Student',
        'is_edit': False,
    })


@login_required
def student_update(request, pk):
    """Render and process the Edit Student form."""
    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            student = form.save()
            messages.success(
                request,
                f"Student record for '{student.full_name}' ({student.student_id}) has been updated successfully!"
            )
            return redirect('student_detail', pk=student.pk)
        else:
            messages.error(request, "Update failed. Please correct the form errors below.")
    else:
        form = StudentForm(instance=student)

    return render(request, 'students/student_form.html', {
        'form': form,
        'student': student,
        'title': f'Edit Student: {student.full_name}',
        'is_edit': True,
    })


@login_required
def student_delete(request, pk):
    """
    Handle deletion of student record.
    Supports direct POST request (from confirmation modal)
    and fallback GET confirmation page.
    """
    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        name = student.full_name
        stu_id = student.student_id
        student.delete()
        messages.success(request, f"Student '{name}' ({stu_id}) was successfully deleted.")
        return redirect('student_list')

    return render(request, 'students/student_confirm_delete.html', {'student': student})
