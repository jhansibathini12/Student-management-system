"""
REST API views for Student Management System.

Provides endpoints for:
- GET    /api/students/        (List all students with optional search/filter)
- POST   /api/students/        (Create a new student record)
- GET    /api/students/<id>/   (Retrieve a single student by numeric ID or student_id)
- PUT    /api/students/<id>/   (Full update of student record)
- PATCH  /api/students/<id>/   (Partial update of student record)
- DELETE /api/students/<id>/   (Delete a student record)
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import Student
from .serializers import StudentSerializer


def get_student_object(identifier):
    """
    Helper function to retrieve a Student object either by
    numeric primary key (id) or string (student_id like 'STU0001').
    Returns None if not found.
    """
    if str(identifier).isdigit():
        try:
            return Student.objects.get(pk=int(identifier))
        except Student.DoesNotExist:
            pass

    # Fallback to matching student_id (case-insensitive)
    try:
        return Student.objects.get(student_id__iexact=str(identifier))
    except Student.DoesNotExist:
        return None


class StudentListCreateAPIView(APIView):
    """
    API endpoint for listing students and creating new student records.

    GET /api/students/
      Optional query params:
      - search: string to search across name, email, or course
      - course: exact course name to filter by

    POST /api/students/
      JSON payload with student details.
    """

    def get(self, request):
        queryset = Student.objects.all()

        # Handle search query (searches name, email, and course)
        search_query = request.query_params.get('search', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(full_name__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(course__icontains=search_query) |
                Q(student_id__icontains=search_query)
            )

        # Handle course filter
        course_filter = request.query_params.get('course', '').strip()
        if course_filter:
            queryset = queryset.filter(course__iexact=course_filter)

        serializer = StudentSerializer(queryset, many=True)
        return Response({
            "status": "success",
            "count": queryset.count(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            student = serializer.save()
            return Response({
                "status": "success",
                "message": f"Student '{student.full_name}' created successfully with ID {student.student_id}.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": "error",
            "message": "Validation failed for student creation.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class StudentDetailAPIView(APIView):
    """
    API endpoint to retrieve, update, or delete an individual student record.
    Supports either integer ID or string student_id (e.g., '1' or 'STU0001').

    GET    /api/students/<id>/
    PUT    /api/students/<id>/
    PATCH  /api/students/<id>/
    DELETE /api/students/<id>/
    """

    def get(self, request, identifier):
        student = get_student_object(identifier)
        if not student:
            return Response({
                "status": "error",
                "message": f"Student with ID '{identifier}' was not found."
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = StudentSerializer(student)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def put(self, request, identifier):
        """Full update of student record."""
        student = get_student_object(identifier)
        if not student:
            return Response({
                "status": "error",
                "message": f"Student with ID '{identifier}' was not found."
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Student record updated successfully.",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "status": "error",
            "message": "Validation failed during update.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, identifier):
        """Partial update of student record."""
        student = get_student_object(identifier)
        if not student:
            return Response({
                "status": "error",
                "message": f"Student with ID '{identifier}' was not found."
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Student record partially updated successfully.",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "status": "error",
            "message": "Validation failed during partial update.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, identifier):
        """Delete student record."""
        student = get_student_object(identifier)
        if not student:
            return Response({
                "status": "error",
                "message": f"Student with ID '{identifier}' was not found."
            }, status=status.HTTP_404_NOT_FOUND)

        student_name = student.full_name
        student_id = student.student_id
        student.delete()
        return Response({
            "status": "success",
            "message": f"Student '{student_name}' ({student_id}) deleted successfully."
        }, status=status.HTTP_200_OK)
