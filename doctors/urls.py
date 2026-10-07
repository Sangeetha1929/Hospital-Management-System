from django.urls import path
from . import views

urlpatterns = [
    path('', views.doctor_list, name='doctor_list'),
    path('<int:pk>/', views.doctor_detail, name='doctor_detail'),
    path('add/', views.doctor_create, name='doctor_create'),
    path('<int:pk>/edit/', views.doctor_update, name='doctor_update'),
    path('<int:pk>/delete/', views.doctor_delete, name='doctor_delete'),
]
