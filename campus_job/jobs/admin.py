from django.contrib import admin
from .models import *

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ('org_name', 'department', 'user')
    search_fields = ('org_name',)
    list_filter = ('department',)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'employer', 'job_type', 'category', 'posted_at', 'remote')
    search_fields = ('title', 'description')
    list_filter = ('job_type', 'category', 'remote')
    date_hierarchy = 'posted_at'


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'study_program', 'year')
    list_filter = ('role', 'year')
    search_fields = ('user__username', 'study_program')


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    search_fields = ('title', 'user__username')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'user', 'status', 'applied_at', 'updated_at')
    list_filter = ('status', 'applied_at')
    search_fields = ('user__username', 'job__title')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('building', 'room', 'address')
    search_fields = ('building', 'address')


@admin.register(InternshipProgram)
class InternshipProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')
    date_hierarchy = 'start_date'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'application', 'sent_at')
    search_fields = ('sender__username', 'recipient__username')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'read', 'created_at')
    list_filter = ('read',)
    search_fields = ('user__username', 'content')
