from django.shortcuts import render, get_object_or_404, redirect

from .decorators import unauthenticated_user
from .forms import RegisterForm, ResumeForm
from .models import Job, Resume, Application, Profile, Employer
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import JobForm

# Главная — список вакансий
@login_required
def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'jobs/jobs.html', {'jobs': jobs})

# Детали вакансии
@login_required
def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    return render(request, 'jobs/job_detail.html', {'job': job})

# Подать заявку
@login_required
def apply_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    resumes = Resume.objects.filter(user=request.user)
    if request.method == 'POST':
        resume_id = request.POST.get('resume')
        cover_letter = request.POST.get('cover_letter', '')
        resume = get_object_or_404(Resume, pk=resume_id)
        Application.objects.create(
            job=job,
            user=request.user,
            resume=resume,
            cover_letter=cover_letter
        )
        return render(request, 'jobs/apply_success.html', {'job': job})
    return render(request, 'jobs/apply_form.html', {'job': job, 'resumes': resumes})

# Мои заявки — список заявок пользователя
@login_required
def my_applications(request):
    applications = Application.objects.filter(user=request.user)
    return render(request, 'jobs/applications.html', {'applications': applications})


@unauthenticated_user
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            Profile.objects.get_or_create(user=user, defaults={'role': 'student'})

            return redirect('profile')
    else:
        form = RegisterForm()

    return render(request, 'jobs/register.html', {'form': form})


@unauthenticated_user
def landing_view(request):
    return render(request, 'jobs/landing.html')

@login_required
def profile_view(request):
    profile = request.user.profile

    if profile.role == 'student':
        return redirect('job_list')

    elif profile.role == 'employer':
        employer, created = Employer.objects.get_or_create(
            user=request.user,
            defaults={'org_name': 'Моя организация', 'description': ''}
        )

        jobs = Job.objects.filter(employer=employer)

        applications = Application.objects.filter(job__in=jobs)

        return render(request, 'jobs/profile_employer.html', {
            'jobs': jobs,
            'applications': applications
        })


@login_required
def accept_application(request, app_id):
    app = get_object_or_404(Application, id=app_id)
    if request.user != app.job.employer:
        return HttpResponseForbidden()
    app.status = 'accepted'
    app.save()
    return redirect('profile')

@login_required
def reject_application(request, app_id):
    app = get_object_or_404(Application, id=app_id)
    if request.user != app.job.employer:
        return HttpResponseForbidden()
    app.status = 'rejected'
    app.save()
    return redirect('profile')


@login_required
def job_create(request):
    # Проверяем, что пользователь — работодатель
    if request.user.profile.role != 'employer':
        return redirect('profile')

    # Получаем или создаём объект Employer
    employer, _ = Employer.objects.get_or_create(
        user=request.user,
        defaults={'org_name': 'Моя организация'}
    )

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = employer
            job.save()
            return redirect('profile')
    else:
        form = JobForm()

    return render(request, 'jobs/job_create.html', {'form': form})


@login_required
def resume_create(request):
    if request.user.profile.role != 'student':
        return redirect('profile')

    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            return redirect('profile')  # или на apply_form, если нужно
    else:
        form = ResumeForm()

    return render(request, 'jobs/resume_create.html', {'form': form})