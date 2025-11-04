from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from jobs.models import Job, Resume, Application, JobCategory, Employer, Department

class APITests(APITestCase):
    def setUp(self):
        # Пользователь и департамент
        self.user = User.objects.create_user(username='student', password='pass1234')
        self.dept = Department.objects.create(name='CS')
        self.employer = Employer.objects.create(user=self.user, org_name='Tech Corp', department=self.dept)
        self.category = JobCategory.objects.create(name='Internship')
        self.job = Job.objects.create(
            title='Test Job',
            description='Job description',
            employer=self.employer,
            category=self.category,
            job_type='full-time'
        )
        self.resume = Resume.objects.create(user=self.user, title='CV', content='My CV')

    # 1. Тест списка вакансий
    def test_job_list(self):
        url = reverse('api-jobs-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Job', str(response.data))

    # 2. Тест деталей вакансии
    def test_job_detail(self):
        url = reverse('api-jobs-detail', kwargs={'pk': self.job.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Test Job')

    # 3. Тест неавторизованного создания заявки
    def test_application_create_unauthenticated(self):
        url = reverse('api-jobs-apply', kwargs={'pk': self.job.id})
        data = {'resume': self.resume.id, 'cover_letter': 'Hello'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 403)

    # 4. Тест успешного создания заявки
    def test_application_create_authenticated(self):
        self.client.login(username='student', password='pass1234')
        url = reverse('api-jobs-apply', kwargs={'pk': self.job.id})
        data = {'resume': self.resume.id, 'cover_letter': 'Hello', 'job': self.job.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Application.objects.count(), 1)

    # 5. Тест списка заявок для пользователя
    def test_application_list(self):
        self.client.login(username='student', password='pass1234')
        Application.objects.create(job=self.job, user=self.user, resume=self.resume)
        url = reverse('api-applications-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    # 6. Тест валидации — создание заявки без резюме
    def test_application_create_missing_resume(self):
        self.client.login(username='student', password='pass1234')
        url = reverse('api-jobs-apply', kwargs={'pk': self.job.id})
        data = {'cover_letter': 'Hello'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)

    # 7. Тест фильтрации вакансий по категории
    def test_job_filter_category(self):
        url = reverse('api-jobs-list') + f'?category={self.category.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Job', str(response.data))
