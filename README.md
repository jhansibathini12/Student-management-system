# 🎓 Student Management System (SMS)

A complete, beginner-friendly, and professional web application built using **Python**, **Django**, **Django REST Framework (DRF)**, **SQLite**, and **Bootstrap 5**.

Designed with a modern **blue-and-white** theme, this system provides a full administrative dashboard, student directory, search & filtering, full CRUD (Create, Read, Update, Delete) capabilities, user authentication, and a complete REST API tested for Postman.

---

## 🌟 Key Features

- **📊 Modern Dashboard**:
  - Real-time summary cards: Total Students, Total Courses, Male/Female enrollment statistics.
  - Interactive top course enrollment breakdown.
  - Recently added students timeline.
  - Responsive table showing student records with quick action buttons.

- **🧑‍🎓 Student Management (CRUD)**:
  - **Add Student**: Clean form with validation (realistic age bounds, phone numbers, unique email).
  - **Auto-generated Student ID**: Sequential unique IDs (e.g., `STU0001`, `STU0002`).
  - **View Student**: Detailed profile view with academic and contact details.
  - **Edit Student**: Pre-filled update form with real-time error handling.
  - **Delete Student**: Two-factor safety with an interactive Bootstrap confirmation modal and fallback GET confirmation page.
  - **Search & Filter**: Search by student name, email, student ID, or course, plus dropdown course filtering with pagination.

- **🔐 Authentication**:
  - Secure user registration and login forms with Bootstrap 5 styling.
  - Session-based authentication with automatic redirect protection (`@login_required`).
  - Dismissible alert notifications for successful actions and validation errors.

- **⚡ REST API with Django REST Framework**:
  - Standardized JSON responses for all CRUD operations.
  - Dual lookup support: search student records by numeric database ID (e.g., `1`) or student identifier (e.g., `STU0001`).
  - Filter by course and search query parameters.
  - Ready for Postman and front-end integration.

---

## 📁 Project Folder Structure

```
project/
├── manage.py                     # Django's administrative command-line utility
├── requirements.txt              # Project dependencies
├── README.md                     # Documentation & setup guide
├── db.sqlite3                    # SQLite database (auto-created on migrate)
├── student_system/               # Project configuration directory
│   ├── __init__.py
│   ├── settings.py               # Global settings, apps, templates, database
│   ├── urls.py                   # Master URL routing
│   ├── asgi.py                   # ASGI entrypoint for async servers
│   └── wsgi.py                   # WSGI entrypoint for web servers
├── students/                     # Main Student Management application
│   ├── __init__.py
│   ├── admin.py                  # Django Admin model registration & customization
│   ├── apps.py                   # App configuration
│   ├── models.py                 # Student database model & auto-ID generator
│   ├── forms.py                  # Bootstrap forms for Student & Auth
│   ├── serializers.py            # DRF Serializers for JSON transformation & validation
│   ├── views.py                  # Web views (Dashboard, CRUD, Authentication)
│   ├── api_views.py              # REST API views (ListCreate, RetrieveUpdateDestroy)
│   ├── urls.py                   # Web frontend routes
│   ├── api_urls.py               # REST API routes (/api/students/...)
│   ├── tests.py                  # Automated test suite (14 unit tests)
│   ├── migrations/               # Database migration files
│   └── management/
│       └── commands/
│           └── seed_data.py      # Seed command for demo data & admin superuser
├── static/                       # Static assets
│   ├── css/
│   │   └── style.css             # Custom styles: blue-and-white theme, cards, tables
│   └── js/
│       └── main.js               # Modal handlers, auto-dismiss alerts, sidebar toggle
└── templates/                    # HTML5 templates (Bootstrap 5)
    ├── base.html                 # Master layout (sidebar, topbar, messages, modal)
    ├── registration/
    │   ├── login.html            # User login page
    │   └── register.html         # User registration page
    └── students/
        ├── dashboard.html        # Dashboard with statistics & recent records
        ├── student_list.html     # Student directory with search, filter & pagination
        ├── student_detail.html   # Student profile view
        ├── student_form.html     # Reusable Add & Edit form
        └── student_confirm_delete.html # Fallback delete confirmation page
```

---

## 📖 Plain English Guide to Important Django Files

If you are new to Django, here is what each core file does:

1. **`models.py`**:
   - Represents your database tables using Python classes.
   - The `Student` class defines columns like `full_name`, `email`, `phone`, `age`, `gender`, `course`, `address`, and `date_of_joining`.
   - The `save()` method in this file automatically assigns a neat ID like `STU0001` before inserting into SQLite.

2. **`views.py`**:
   - Contains the business logic that handles web browser requests and returns HTML pages.
   - For example, `dashboard()` queries the database for student counts and renders `dashboard.html`.

3. **`forms.py`**:
   - Handles HTML form inputs, field sanitization, and server-side validation.
   - Ensures ages are realistic, phone numbers have valid digit lengths, and emails are unique.

4. **`serializers.py`**:
   - Bridges the gap between Python model objects and JSON format required by mobile apps and APIs.
   - Converts incoming JSON requests into validated Python dictionaries.

5. **`api_views.py`**:
   - Provides REST API endpoints that return pure JSON data instead of HTML templates.
   - Handles `GET`, `POST`, `PUT`, `PATCH`, and `DELETE` requests for external tools like Postman.

6. **`urls.py` & `api_urls.py`**:
   - The "address book" of your application. When a user visits `http://127.0.0.1:8000/students/`, this file routes the request to the `student_list` view.

7. **`admin.py`**:
   - Configures the built-in Django Admin portal (`/admin/`), enabling quick searching, filtering, and bulk management.

8. **`settings.py`**:
   - The master configuration file where database settings, installed applications, template directories, and authentication routes are registered.

---

## 🚀 Setup & Execution Guide

### Prerequisites
- **Python 3.10+** (Tested on Python 3.12 / 3.14).
- Ensure Python and pip are added to your system `PATH`.

---

### Step 1: Open the Project in VS Code
1. Launch **Visual Studio Code**.
2. Click **File** &rarr; **Open Folder...** and select:
   ```
   C:\Users\jhansibathini\Documents\project
   ```
3. Open a new terminal in VS Code:
   - Shortcut: `` Ctrl + ` `` (Backtick) or go to **Terminal** &rarr; **New Terminal**.

---

### Step 2: (Optional but Recommended) Create a Virtual Environment
In the VS Code terminal, run:

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

*(If execution policy restricts running scripts, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first).*

---

### Step 3: Install Required Packages
Install the required packages listed in `requirements.txt`:
```powershell
pip install -r requirements.txt
```

---

### Step 4: Run Database Migrations
Create the SQLite database tables:
```powershell
python manage.py makemigrations students
python manage.py migrate
```

---

### Step 5: Start the Django Development Server
Launch the local web server:
```powershell
python manage.py runserver
```

Open your browser and visit:
👉 **http://127.0.0.1:8000/**

### Step 6: Create an Account & Log In
1. On the login page, click **"Sign Up"** or visit **http://127.0.0.1:8000/register/**.
2. Fill in your Name, Username, Email, and Password, then click **Complete Registration**.
3. You will be redirected to the login page with a success message.
4. Log in using the credentials you just created to access the full Dashboard!

---

## 🧪 Running Automated Tests

Run the built-in test suite to verify models, web views, and REST API endpoints:
```powershell
python manage.py test students
```

Expected result:
```
Ran 14 tests in 0.5s
OK
```

---

## 📡 REST API Documentation

Base URL: `http://127.0.0.1:8000/api/`

| HTTP Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/students/` | List all students (supports `?search=` and `?course=`) |
| `POST` | `/api/students/` | Create a new student |
| `GET` | `/api/students/<id>/` | Retrieve student details (by ID e.g. `1` or `STU0001`) |
| `PUT` | `/api/students/<id>/` | Full update of student record |
| `PATCH` | `/api/students/<id>/` | Partial update of student record |
| `DELETE` | `/api/students/<id>/` | Permanently delete student record |

---

### 1. List All Students
- **URL**: `GET http://127.0.0.1:8000/api/students/`
- **Query Parameters**:
  - `search` *(optional)*: Search across name, email, course, or student ID.
  - `course` *(optional)*: Filter by exact course name (e.g. `Computer Science`).

**Example Response (200 OK):**
```json
{
  "status": "success",
  "count": 10,
  "data": [
    {
      "id": 1,
      "student_id": "STU0001",
      "full_name": "Aarav Sharma",
      "email": "aarav.sharma@example.com",
      "phone": "+1 (555) 234-5678",
      "age": 20,
      "gender": "Male",
      "course": "Computer Science",
      "address": "402 Tech Park Boulevard, Austin, TX",
      "date_of_joining": "2025-08-15",
      "created_at": "2026-11-12T06:19:24.123456Z",
      "updated_at": "2026-11-12T06:19:24.123456Z"
    }
  ]
}
```

---

### 2. Create Student
- **URL**: `POST http://127.0.0.1:8000/api/students/`
- **Headers**: `Content-Type: application/json`

**Sample Request Body:**
```json
{
  "full_name": "Kavya Patel",
  "email": "kavya.patel@example.com",
  "phone": "+1 (555) 888-4321",
  "age": 21,
  "gender": "Female",
  "course": "Artificial Intelligence",
  "address": "500 Innovation Way, Boston, MA",
  "date_of_joining": "2026-03-01"
}
```

**Example Response (201 Created):**
```json
{
  "status": "success",
  "message": "Student 'Kavya Patel' created successfully with ID STU0011.",
  "data": {
    "id": 11,
    "student_id": "STU0011",
    "full_name": "Kavya Patel",
    "email": "kavya.patel@example.com",
    "phone": "+1 (555) 888-4321",
    "age": 21,
    "gender": "Female",
    "course": "Artificial Intelligence",
    "address": "500 Innovation Way, Boston, MA",
    "date_of_joining": "2026-03-01",
    "created_at": "2026-11-12T06:25:00.000000Z",
    "updated_at": "2026-11-12T06:25:00.000000Z"
  }
}
```

---

### 3. Retrieve Student
- **URL**: `GET http://127.0.0.1:8000/api/students/1/` (or `/api/students/STU0001/`)

**Example Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "id": 1,
    "student_id": "STU0001",
    "full_name": "Aarav Sharma",
    "email": "aarav.sharma@example.com",
    "phone": "+1 (555) 234-5678",
    "age": 20,
    "gender": "Male",
    "course": "Computer Science",
    "address": "402 Tech Park Boulevard, Austin, TX",
    "date_of_joining": "2025-08-15"
  }
}
```

---

### 4. Update Student (Full PUT or Partial PATCH)
- **URL**: `PATCH http://127.0.0.1:8000/api/students/1/`
- **Headers**: `Content-Type: application/json`

**Sample Request Body:**
```json
{
  "phone": "+1 (555) 999-8888",
  "age": 21
}
```

**Example Response (200 OK):**
```json
{
  "status": "success",
  "message": "Student record partially updated successfully.",
  "data": {
    "id": 1,
    "student_id": "STU0001",
    "full_name": "Aarav Sharma",
    "phone": "+1 (555) 999-8888",
    "age": 21
  }
}
```

---

### 5. Delete Student
- **URL**: `DELETE http://127.0.0.1:8000/api/students/1/`

**Example Response (200 OK):**
```json
{
  "status": "success",
  "message": "Student 'Aarav Sharma' (STU0001) deleted successfully."
}
```

---

## 📮 Postman Testing Step-by-Step

You can test the APIs directly in **Postman**:

1. **Open Postman** and create a new Collection called `Student Management API`.
2. **Add Request: List Students**
   - Method: `GET`
   - URL: `http://127.0.0.1:8000/api/students/`
   - Click **Send**.
3. **Add Request: Create Student**
   - Method: `POST`
   - URL: `http://127.0.0.1:8000/api/students/`
   - Go to **Body** tab &rarr; select **raw** &rarr; select **JSON**.
   - Paste the sample JSON payload from Section 2 above and click **Send**.
4. **Add Request: Update Student**
   - Method: `PATCH`
   - URL: `http://127.0.0.1:8000/api/students/1/`
   - Body: `{"phone": "+1 (555) 000-1111"}`
   - Click **Send**.
5. **Add Request: Delete Student**
   - Method: `DELETE`
   - URL: `http://127.0.0.1:8000/api/students/1/`
   - Click **Send**.

---

## 🛡️ Django Admin Interface

To access the Django Admin portal:
1. Make sure the server is running (`python manage.py runserver`).
2. Navigate to: **http://127.0.0.1:8000/admin/**
3. Log in with:
   - **Username:** `admin`
   - **Password:** `admin123`
4. From the admin dashboard, you can perform full administration, search across student fields, and filter by courses.
