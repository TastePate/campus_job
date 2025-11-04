from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="CampusJobs API",
      default_version='v1',
      description="API для поиска вакансий и подачи заявок",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('jobs.urls')),        # фронтенд HTML
    path('api/', include('jobs.api_urls')), # DRF API
]
