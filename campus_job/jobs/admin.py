from django.contrib import admin
from .models import Department, JobCategory, Tag, Employer, Job, JobTag

admin.site.register([Department, JobCategory, Tag, Employer, Job, JobTag])