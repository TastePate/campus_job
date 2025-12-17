from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.landing_view, name='landing'),
    path('profile/', views.profile_view, name='profile'),
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/<int:pk>/', views.job_detail, name='job-detail'),
    path('jobs/<int:pk>/apply/', views.apply_job, name='apply-job'),
    path('applications/', views.my_applications, name='applications'),
    path('application/<int:app_id>/accept/', views.accept_application, name='accept_application'),
    path('application/<int:app_id>/reject/', views.reject_application, name='reject_application'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('jobs/create/', views.job_create, name='job_create'),
    path('resume/create/', views.resume_create, name='resume_create'),
    path('employer/profile/edit/', views.employer_profile_edit, name='employer_profile_edit'),
    path('resume/<int:resume_id>/edit/', views.resume_edit, name='resume_edit'),
    path('resume/<int:resume_id>/delete/', views.resume_delete, name='resume_delete'),
    path('application/<int:app_id>/detail/', views.application_detail, name='application_detail'),
    path('notifications/mark-read/', views.mark_notifications_read, name='mark_notifications_read'),
    path('api/notifications/', views.get_notifications, name='get_notifications'),
    path('jobs/<int:job_id>/edit/', views.job_edit, name='job_edit'),
    path('jobs/<int:job_id>/delete/', views.job_delete, name='job_delete'),
]