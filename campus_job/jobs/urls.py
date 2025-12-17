from django.urls import path
from .api_views import JobListView, JobDetailView, ApplicationCreateView, ApplicationListView
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.landing_view, name='landing'),  # Главная
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/<int:pk>/', views.job_detail, name='job-detail'),  # Детали вакансии
    path('jobs/<int:pk>/apply/', views.apply_job, name='apply-job'),  # Подать заявку
    path('applications/', views.my_applications, name='applications'),  # Мои заявки
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='jobs/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout')
]