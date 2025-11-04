from django.urls import path
from .api_views import JobListView, JobDetailView, ApplicationCreateView, ApplicationListView
from . import views


urlpatterns = [
    path('', views.index, name='index'),  # Главная
    path('jobs/<int:pk>/', views.job_detail, name='job-detail'),  # Детали вакансии
    path('jobs/<int:pk>/apply/', views.apply_job, name='apply-job'),  # Подать заявку
    path('applications/', views.my_applications, name='applications'),  # Мои заявки
]