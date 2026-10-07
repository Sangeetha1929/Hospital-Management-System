# CityCare Hospital Management System

A simple, beginner-friendly **Hospital Management System** built with **Django**, **SQLite**, **HTML**, **CSS**, and **Vanilla JavaScript**. It lets guests browse doctors, patients book and manage appointments, and staff (admin) manage everything.

The project is split into **four Django apps**, each responsible for one area:

| App | Responsibility |
| --- | --- |
| `core` | Landing page, authentication (register / login / logout), user profile |
| `doctors` | Doctor CRUD (list, detail, add, edit, delete) |
| `patients` | Patient records + patient dashboard |
| `appointments` | Appointment booking, listing, cancel, status updates |

Built **without Bootstrap** or any CSS framework — all styling is custom, fully responsive, and professional.

---

## Features

### 1. Home Page
- Hospital name (CityCare Hospital) with a logo
- Responsive navbar (hamburger menu on mobile)
- About Us section with hospital stats
- Services section (cardiology, neurology, pediatrics, etc.)
- Featured Doctors section
- Contact section with a validated message form

### 2. User Authentication
- Register (choose Patient or Staff type)
- Login
- Logout
- Profile page (edit name, email, phone, address)

### 3. Doctors
- Add doctor (staff only)
- View all doctors (everyone)
- Edit doctor (staff only)
- Delete doctor (staff only)
- Doctor detail page with contact, experience and bio

### 4. Patients
- Patient registration (part of account registration)
- Patient profile (medical & contact details)
- Patient dashboard (stats + appointment list)

### 5. Appointments
- Book appointment (choose doctor, date, time, reason)
- View appointments (patient sees own, staff sees all)
- Cancel appointment
- Appointment status: `Pending → Confirmed → Completed` / `Cancelled`

### 6. Staff / Admin
- Manage doctors (add / edit / delete)
- Manage patients (view all, view details, delete)
- Manage appointments (confirm, complete, cancel)

### 7. Permissions (Role-Based Access)
| Role | Allowed |
| --- | --- |
| **Guest** (not logged in) | View doctors only |
| **Patient** | Book and manage **their own** appointments + manage their profile |
| **Staff** | Manage doctors, patients and all appointments |

### 8. Database Models
- `Profile` (`core`) — linked 1-to-1 to Django's `User`; stores user type (patient/staff), phone, address
- `Doctor` (`doctors`) — name, specialization, department, phone, email, experience, availability, bio
- `Patient` (`patients`) — linked 1-to-1 to `User`; DOB, gender, blood group, emergency contact, medical notes
- `Appointment` (`appointments`) — links a `Patient` to a `Doctor`; date, time, reason, status

### 9. Django Usage
| Concern | Location |
| --- | --- |
| `Profile` model + auth views | `core/` |
| `Doctor` model + CRUD views | `doctors/` |
| `Patient` model + dashboard views | `patients/` |
| `Appointment` model + booking views | `appointments/` |
| **Templates** | Django template language with `base.html` inheritance |
| **Admin** | One admin module per app |

---

## Tech Stack

- **Python 3** + **Django** (tested on Django 6.x)
- **SQLite** (database, zero setup required)
- **HTML5 / CSS3** — custom stylesheet, fully responsive, no frameworks
- **Vanilla JavaScript** — mobile menu, auto-dismiss alerts, form validation

---

## Project Structure

```
Hospital_Management/
├── manage.py                       # Django CLI entry point
├── db.sqlite3                      # SQLite database (auto-created)
├── hospital_management/            # PROJECT configuration package
│   ├── __init__.py
│   ├── settings.py                 # apps, templates, static, login/logout config
│   ├── urls.py                     # ROOT URLconf — includes core, doctors, patients, appointments
│   ├── wsgi.py                     # WSGI entry for servers
│   └── asgi.py                     # ASGI entry (async)
│
├── core/                           # auth + landing + profile
│   ├── admin.py                    # registers User with Profile inline
│   ├── models.py                   # Profile (1-to-1 with User)
│   ├── forms.py                    # RegisterForm, ProfileForm
│   ├── views.py                    # home, register, profile (+ role helpers)
│   ├── urls.py                     # home, register, login, logout, profile
│   └── migrations/
│
├── doctors/                        # doctor records
│   ├── admin.py                    # registers Doctor
│   ├── models.py                   # Doctor
│   ├── forms.py                    # DoctorForm
│   ├── views.py                    # doctor_list / detail / create / update / delete
│   ├── urls.py                     # CRUD routes (list, detail, add, edit, delete)
│   └── migrations/
│
├── patients/                       # patient records + dashboard
│   ├── admin.py                    # registers Patient
│   ├── models.py                   # Patient (1-to-1 with User)
│   ├── forms.py                    # PatientForm
│   ├── views.py                    # dashboard, update, list, detail, delete
│   ├── urls.py                     # list, detail, delete
│   └── migrations/
│
├── appointments/                   # appointment booking
│   ├── admin.py                    # registers Appointment
│   ├── models.py                   # Appointment (FK → Patient, Doctor)
│   ├── forms.py                    # AppointmentForm
│   ├── views.py                    # create, list, cancel, update_status
│   ├── urls.py                     # list, book, cancel, status
│   └── migrations/
│
├── templates/                      # ALL HTML templates
│   ├── base.html                   # main layout (inherited everywhere)
│   ├── home.html                   # landing page
│   ├── login.html
│   ├── register.html
│   ├── profile.html
│   ├── doctors/
│   │   ├── doctor_list.html
│   │   ├── doctor_detail.html
│   │   ├── doctor_form.html          # add + edit (shared)
│   │   └── doctor_confirm_delete.html
│   ├── patients/
│   │   ├── patient_list.html
│   │   ├── patient_detail.html
│   │   ├── patient_dashboard.html
│   │   ├── patient_form.html         # edit medical details
│   │   └── patient_confirm_delete.html
│   └── appointments/
│       ├── appointment_list.html
│       ├── appointment_form.html     # booking
│       └── appointment_confirm_delete.html  # cancel confirmation
└── static/                        # STATIC ASSETS (served in development)
    └── css/
        └── style.css              # custom, responsive CSS (no Bootstrap, no JS)
```

---

## URL Routing Layout

```
hospital_management/urls.py  (ROOT)
├── admin/                    → Django admin
├── ''                        → core.urls      (home, register, login, logout, profile)
├── doctors/                  → doctors.urls    (list, detail, add, edit, delete)
├── patient/dashboard/        → patient (staff-protected) dashboard
├── patient/edit/             → patient update
├── patients/                 → patients.urls   (list, detail, delete)
└── appointments/             → appointments.urls (list, book, cancel, status)
```

---

## Setup & Installation (Step by Step)

Follow these steps **in order**.

### Step 1 — Install Python
Make sure **Python 3.10+** is installed:

```bash
python --version
```

### Step 2 — Install Django

```bash
pip install django
```

### Step 3 — (Optional) Create a Virtual Environment
A virtual environment keeps dependencies isolated. Recommended for any real project.

```bash
python -m venv venv

# Activate it:
#   Windows (PowerShell)
venv\Scripts\Activate.ps1
#   Windows (CMD)
venv\Scripts\activate.bat
#   macOS / Linux
source venv/bin/activate
```

Then install Django inside it:

```bash
pip install django
```

### Step 4 — Navigate to the Project Folder

```bash
cd Hospital_Management
```

### Step 5 — Create the Database Tables

```bash
python manage.py makemigrations
python manage.py migrate
```

- `makemigrations` creates migration files for your models.
- `migrate` applies them and creates `db.sqlite3`.

### Step 6 — Create a Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Enter a **username**, **email**, and **password**. This account can log into `/admin/`.
> Follow the message: "Superuser created successfully."

### Step 7 — Run the Development Server

```bash
python manage.py runserver
```

Open your browser at: **http://127.0.0.1:8000/**

### Step 8 — Make the Superuser a Staff User
Django's superuser is *not* automatically a Hospital "Staff" — the hospital uses its own role stored in `Profile.user_type`.

1. Log in at **http://127.0.0.1:8000/admin/**
2. Find **Profiles** → click your superuser's profile row
3. Change **User type** from `Patient` to `Staff`
4. Click **Save**

Now log out of `/admin/` and log in on the main site — you will see the staff menu (Manage Patients, Manage Appointments, Add Doctor).

---

## How the Workflow Works (Step by Step)

### A. Guest (Visitor) Workflow
1. Open **http://127.0.0.1:8000/** → landing page with About, Services, Doctors, Contact.
2. Click **Doctors** in the navbar → see all doctors.
3. Click **View Details** on any doctor → full profile (contact, experience, availability).
4. Guests **cannot** book appointments or access dashboards — they are redirected to the login page.

### B. Registration & Login Workflow
1. Click **Register** in the navbar.
2. Fill in username, name, email, password, phone and choose a **user type**:
   - **Patient** → gets a patient dashboard + can book appointments.
   - **Staff** → gets management menus (doctors, patients, appointments).
3. Submit → account is created, a `Profile` is auto-created (Django signal), a `Patient` record is auto-created for patients, and you are **logged in automatically**.
4. **Logout** → click Logout in the navbar (POST form).
5. **Login** → click Login, enter credentials → redirected to home.
6. **Profile** → click your username → edit name, email, phone, address.

### C. Patient Workflow
1. After registering as a **Patient**, open **Dashboard** from the navbar.
2. **Edit Details** → fill DOB, gender, blood group, emergency contact, address, medical notes.
3. **Book Appointment**:
   - Choose doctor, date, time, reason.
   - Appointment is saved with status **Pending**.
4. **Appointments** page → view your own appointments, filter by status.
5. **Cancel** → click Cancel → confirm → status becomes **Cancelled**.
6. Completed / cancelled appointments can no longer be changed.

### D. Staff (Admin) Workflow
1. Log in with a **Staff** user type.
2. **Add Doctor** → fill the form → doctor appears on the public site.
3. **Doctors** page → Edit or Delete any doctor.
4. **Patients** page → search patients, view details, delete a patient (removes their account too).
5. **Appointments** page → see appointments from all patients:
   - **Confirm** → `Pending` → `Confirmed`
   - **Complete** → `Confirmed` → `Completed`
   - Or directly **Cancel** an appointment.
6. **Django Admin** (`/admin/`) → full control of all data incl. changing user types.

### E. Appointment Status Lifecycle

```
Pending  ──►  Confirmed  ──►  Completed
   └────────────►  Cancelled
```

- Booked by patient → `Pending`
- Confirmed by staff → `Confirmed`
- Marked done by staff → `Completed`
- Cancelled by patient **or** staff → `Cancelled`

---

## Permissions / Access Matrix

| URL | Guest | Patient | Staff |
| --- | :---: | :---: | :---: |
| `/` (home) | ✅ | ✅ | ✅ |
| `/doctors/` (list) | ✅ | ✅ | ✅ |
| `/doctors/<id>/` (detail) | ✅ | ✅ | ✅ |
| `/doctors/add/` | ❌ | ❌ | ✅ |
| `/doctors/<id>/edit/` | ❌ | ❌ | ✅ |
| `/doctors/<id>/delete/` | ❌ | ❌ | ✅ |
| `/register/`, `/login/` | ✅ | n/a | n/a |
| `/profile/` | ❌ (login) | ✅ | ✅ |
| `/patient/dashboard/` | ❌ | ✅ | ❌ |
| `/patient/edit/` | ❌ | ✅ | ❌ |
| `/patients/` (list) | ❌ | ❌ | ✅ |
| `/patients/<id>/` (detail) | ❌ | ❌ | ✅ |
| `/patients/<id>/delete/` | ❌ | ❌ | ✅ |
| `/appointments/` (list) | ❌ (login) | ✅ (own) | ✅ (all) |
| `/appointments/book/` | ❌ | ✅ | ❌ |
| `/appointments/<id>/cancel/` | ❌ | ✅ (own only) | ✅ |
| `/appointments/<id>/status/<status>/` | ❌ | ❌ | ✅ |
| `/admin/` | ❌ (superuser only) | ❌ | superuser only |

---

## Key Files Explained

### Models
```python
# core/models.py
class Profile(models.Model):      # 1-to-1 with User, adds user_type / phone / address

# doctors/models.py
class Doctor(models.Model):       # doctor records, department choices, availability

# patients/models.py
class Patient(models.Model):      # 1-to-1 with User, medical info

# appointments/models.py
class Appointment(models.Model):  # FK to Patient and Doctor, status choices
```

### Forms
- `core/forms.py` — `RegisterForm` (auth + phone + user type; auto-creates Profile & Patient), `ProfileForm`.
- `doctors/forms.py` — `DoctorForm` (staff CRUD form).
- `patients/forms.py` — `PatientForm` (patient medical details).
- `appointments/forms.py` — `AppointmentForm` (booking form, doctor dropdown from DB).

### Views
- `core/views.py` — `home()`, `register()`, `profile()` + role helpers `is_staff()` / `is_patient()`.
- `doctors/views.py` — `doctor_*` CRUD guarded by `@user_passes_test(is_staff)`.
- `patients/views.py` — `patient_dashboard`, `patient_update`, `patient_list`, `patient_detail`, `patient_delete` guarded by role.
- `appointments/views.py` — `appointment_create`, `appointment_list`, `appointment_cancel`, `appointment_update_status` with ownership checks.

### URLconfigs
Each app has its own `urls.py`, all included from the root `hospital_management/urls.py`:

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('doctors/', include('doctors.urls')),
    path('patient/dashboard/', patients_views.patient_dashboard, name='patient_dashboard'),
    path('patient/edit/', patients_views.patient_update, name='patient_update'),
    path('patients/', include('patients.urls')),
    path('appointments/', include('appointments.urls')),
]
```

### `hospital_management/settings.py`
Key settings:
```python
INSTALLED_APPS = ['...', 'core', 'doctors', 'patients', 'appointments']
TEMPLATES → 'DIRS': [BASE_DIR / 'templates']
STATICFILES_DIRS = [BASE_DIR / 'static']
LOGIN_URL = 'login'
```

### `templates/base.html`
The master layout. Every page extends it:

```django
{% extends 'base.html' %}
{% block content %} ... {% endblock %}
```

It includes: navbar (with role-based links), flash messages, and footer.

---

## Useful Commands

```bash
# Run the server
python manage.py runserver

# Apply model changes to the database
python manage.py makemigrations
python manage.py migrate

# Open an interactive shell with the project loaded
python manage.py shell

# Create an admin user
python manage.py createsuperuser

# Verify the project (no issues = good)
python manage.py check
```

---

## Testing the Application

1. Start the server: `python manage.py runserver`
2. Go to **http://127.0.0.1:8000/**
3. **Guest flow:** browse Doctors.
4. **Register a Patient** → Dashboard → Edit Details → Book Appointment → Appointments → Cancel.
5. **Create staff** via Register with type *Staff*, or change the superuser's profile type in `/admin/`.
6. **Staff flow:** Add Doctor → Confirm appointments → Manage patients.

---

## Troubleshooting

| Problem | Solution |
| --- | --- |
| `No module named 'django'` | Run `pip install django` (and activate venv if you created one). |
| `django-admin` not recognized on PATH | Use `python -m django startproject` instead, or `pip install --user django`. |
| Tables missing | Run `python manage.py makemigrations` then `python manage.py migrate`. |
| Forgot password | `python manage.py createsuperuser` again, or manage from `python manage.py shell`. |
| Static files (CSS) not loading | Confirm `STATICFILES_DIRS = [BASE_DIR / 'static']` in `settings.py` and the folder path `static/css/style.css` exists. |
| Staff menu not showing after superuser login | Superusers are not auto-set to Staff — change `Profile → user_type` to `Staff` in `/admin/`. |
| Login redirects aren't working | Check `LOGIN_URL`, `LOGIN_REDIRECT_URL`, `LOGOUT_REDIRECT_URL` in `settings.py`. |
| URL reverse errors (`NoReverseMatch`) | Make sure each app's `urls.py` is included from `hospital_management/urls.py` and the `{% url %}` names match. |

---

## License

This project is for educational purposes. Feel free to use, learn from, and modify it.