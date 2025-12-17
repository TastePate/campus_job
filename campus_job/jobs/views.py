from django.shortcuts import render, get_object_or_404, redirect

from .forms import RegisterForm
from .models import Job, Resume, Application
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

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


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('jobs')
    else:
        form = RegisterForm()

    return render(request, 'jobs/register.html', {'form': form})


def landing_view(request):
    return render(request, 'jobs/landing.html')