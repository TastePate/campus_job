from django.shortcuts import render, get_object_or_404, redirect
from .models import Job, Resume, Application
from django.contrib.auth.decorators import login_required

# Главная — список вакансий
def index(request):
    jobs = Job.objects.all()
    return render(request, 'jobs/index.html', {'jobs': jobs})

# Детали вакансии
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
