from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('activity/', views.admin_activity_list, name='admin_activity_list'),
    path('users/', views.admin_user_list, name='admin_user_list'),
    path('users/<int:pk>/admin/', views.admin_user_toggle_admin, name='admin_user_toggle_admin'),
    path('users/<int:pk>/delete/', views.admin_user_delete, name='admin_user_delete'),
]
