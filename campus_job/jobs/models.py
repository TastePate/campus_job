from django.db import models
from django.contrib.auth.models import User


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
