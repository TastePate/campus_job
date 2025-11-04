from django.contrib import admin
from .models import *

admin.site.register([Department, JobCategory, Tag, Employer, Job, JobTag])
admin.site.register([Profile, Resume, Application, Location, InternshipProgram, Message, Notification])
