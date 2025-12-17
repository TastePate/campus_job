from django.shortcuts import render, get_object_or_404, redirect

from .decorators import unauthenticated_user
from .forms import RegisterForm, ResumeForm, EmployerForm
from .models import Job, Resume, Application, Profile, Employer, Notification
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
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
        notifications = Notification.objects.filter(user=request.user, read=False).order_by('-created_at')
        resumes = Resume.objects.filter(user=request.user)
        applications = Application.objects.filter(user=request.user).order_by('-applied_at')
        return render(request, 'jobs/profile_student.html', {
            'resumes': resumes,
            'applications': applications,
            'notifications': notifications
        })

    elif profile.role == 'employer':
        notifications = Notification.objects.filter(user=request.user, read=False).order_by('-created_at')
        employer, created = Employer.objects.get_or_create(
            user=request.user,
            defaults={'org_name': 'Моя организация', 'description': ''}
        )

        jobs = Job.objects.filter(employer=employer)

        applications = Application.objects.filter(job__in=jobs)

        return render(request, 'jobs/profile_employer.html', {
            'jobs': jobs,
            'applications': applications,
            'notifications': notifications
        })


@login_required
def accept_application(request, app_id):
    app = get_object_or_404(Application, id=app_id)
    if request.user != app.job.employer.user:
        return HttpResponseForbidden()
    app.status = 'accepted'
    app.save()
    return redirect('profile')

@login_required
def reject_application(request, app_id):
    app = get_object_or_404(Application, id=app_id)
    if request.user != app.job.employer.user:
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


@login_required
def employer_profile_edit(request):
    if request.user.profile.role != 'employer':
        return redirect('profile')

    employer, _ = Employer.objects.get_or_create(
        user=request.user,
        defaults={'org_name': request.user.username + ' Organization'}
    )

    if request.method == 'POST':
        form = EmployerForm(request.POST, instance=employer)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EmployerForm(instance=employer)

    return render(request, 'jobs/employer_profile_edit.html', {'form': form})


@login_required
def resume_edit(request, resume_id):
    if request.user.profile.role != 'student':
        return redirect('profile')

    resume = get_object_or_404(Resume, id=resume_id, user=request.user)

    if request.method == 'POST':
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ResumeForm(instance=resume)

    return render(request, 'jobs/resume_edit.html', {
        'form': form,
        'resume': resume
    })


@login_required
def resume_delete(request, resume_id):
    if request.user.profile.role != 'student':
        return redirect('profile')

    resume = get_object_or_404(Resume, id=resume_id, user=request.user)

    if request.method == 'POST':
        resume.delete()
        return redirect('profile')

    return render(request, 'jobs/resume_delete.html', {'resume': resume})


@login_required
def application_detail(request, app_id):
    application = get_object_or_404(Application, id=app_id)

    if request.user.profile.role != 'employer' or request.user != application.job.employer.user:
        return HttpResponseForbidden()


    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'accept':
            application.status = 'accepted'
        elif action == 'reject':
            application.status = 'rejected'
        application.save(update_fields=['status'])
        return redirect('application_detail', app_id=app_id)

    return render(request, 'jobs/application_detail.html', {
        'application': application,
        'student': application.user,
        'resume': application.resume,
        'job': application.job,
    })

@login_required
def mark_notifications_read(request):
    if request.method == 'POST':
        Notification.objects.filter(user=request.user, read=False).update(read=True)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def get_notifications(request):
    notifications = Notification.objects.filter(
        user=request.user,
        read=False
    ).order_by('-created_at')[:10].values(
        'content', 'created_at'
    )
    return JsonResponse({
        'count': len(list(notifications)),
        'notifications': list(notifications)
    })