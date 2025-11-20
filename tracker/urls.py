from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # 1. The Landing Page is now the default route
    path('', views.home, name='home'),
    
    
    # 2. The Dashboard is moved to specific URL
    path('dashboard/', views.dashboard, name='dashboard'),
    path('resources/', views.resources, name='resources'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='tracker/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # CRUD
    path('add/', views.add_item, name='add_item'),
    path('edit/<int:pk>/', views.edit_item, name='edit_item'),
    path('delete/<int:pk>/', views.delete_item, name='delete_item'),
]