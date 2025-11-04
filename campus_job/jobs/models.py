from django.db import models
from django.contrib.auth.models import User

from django.conf import settings


class Department(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class JobCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Employer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    org_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.org_name


class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ('part_time', 'Part-time'),
        ('full_time', 'Full-time'),
        ('internship', 'Internship'),
        ('volunteer', 'Volunteer'),
    ]

    location = models.ForeignKey('Location', on_delete=models.SET_NULL, null=True, blank=True)
    internship_program = models.ForeignKey('InternshipProgram', on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, null=True)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    posted_at = models.DateField(auto_now_add=True)
    expires_at = models.DateField(null=True, blank=True)
    slots = models.PositiveIntegerField(default=1)
    remote = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class JobTag(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('job', 'tag')

    def __str__(self):
        return f"{self.job.title} — {self.tag.name}"

class Profile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('staff', 'Staff'),
        ('employer', 'Employer'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    study_program = models.CharField(max_length=200, blank=True)
    year = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class Location(models.Model):
    building = models.CharField(max_length=100)
    room = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.building} {self.room}".strip()


class Resume(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resume: {self.title} ({self.user.username})"


class Application(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'),
    ]

    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    resume = models.ForeignKey('Resume', on_delete=models.SET_NULL, null=True)
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} → {self.job.title} ({self.status})"


class InternshipProgram(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name


class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages'
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages'
    )
    application = models.ForeignKey('Application', on_delete=models.CASCADE)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username}"


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"
