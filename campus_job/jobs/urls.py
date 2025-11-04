from django.urls import path
from .api_views import JobListView, JobDetailView, ApplicationCreateView, ApplicationListView

urlpatterns = [
    path('jobs/', JobListView.as_view(), name='api-jobs-list'),
    path('jobs/<int:pk>/', JobDetailView.as_view(), name='api-jobs-detail'),
    path('jobs/<int:pk>/apply/', ApplicationCreateView.as_view(), name='api-jobs-apply'),
    path('applications/', ApplicationListView.as_view(), name='api-applications-list'),
]
