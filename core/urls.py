from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from patients import views as patients_views

urlpatterns = [
    path('', views.home, name='home'),

    path('register/', views.register, name='register'),
    path('login/', views.RoleLoginView.as_view(), name='login'),
    path('admin-login/', views.AdminLoginView.as_view(), name='admin_login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('doctors/', include('doctors.urls')),
    path('patient/dashboard/', patients_views.patient_dashboard, name='patient_dashboard'),
    path('patient/edit/', patients_views.patient_update, name='patient_update'),
    path('patients/', include('patients.urls')),
    path('appointments/', include('appointments.urls')),
    path('admin-panel/', include('adminpanel.urls')),
]
