from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from jobs.models import Job, Resume, Application, JobCategory, Employer, Department



class JobAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.student = User.objects.create_user(username='student', password='pass1234')
        self.student_resume = Resume.objects.create(
            user=self.student,
            title='Junior Developer',
            content='Python, Django, JS'
        )

        self.employer_user = User.objects.create_user(username='employer', password='pass1234')
        self.dept = Department.objects.create(name='Computer Science')
        self.employer = Employer.objects.create(
            user=self.employer_user,
            org_name='Awesome Corp',
            department=self.dept
        )
        self.category = JobCategory.objects.create(name='Software Engineering')

        self.job = Job.objects.create(
            title='Backend Developer',
            description='We need a Python expert',
            employer=self.employer,
            category=self.category,
            job_type='full_time',
            remote=True
        )

    def test_job_list_anonymous(self):
        url = reverse('api-jobs-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Backend Developer')

    def test_job_detail(self):
        url = reverse('api-jobs-detail', kwargs={'pk': self.job.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['remote'])

    def test_application_create_unauthenticated(self):
        url = reverse('api-jobs-apply', kwargs={'pk': self.job.pk})
        data = {'resume': self.student_resume.pk, 'cover_letter': 'Hi'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_application_create_success(self):
        self.client.force_authenticate(user=self.student)
        url = reverse('api-jobs-apply', kwargs={'pk': self.job.pk})
        data = {
            'job': self.job.pk,
            'resume': self.student_resume.pk,
            'cover_letter': 'Я идеально подхожу!'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Application.objects.count(), 1)
        self.assertEqual(Application.objects.first().user, self.student)

    def test_application_create_invalid_resume(self):
        self.client.force_authenticate(user=self.student)
        url = reverse('api-jobs-apply', kwargs={'pk': self.job.pk})
        data = {'resume': 99999, 'cover_letter': 'Hello'}  # несуществующее резюме
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_application_list_authenticated(self):
        self.client.force_authenticate(user=self.student)
        Application.objects.create(
            job=self.job,
            user=self.student,
            resume=self.student_resume,
            cover_letter='Test'
        )
        url = reverse('api-applications-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_application_list_empty_for_other_user(self):
        other_student = User.objects.create_user(username='other', password='pass')
        self.client.force_authenticate(user=other_student)
        url = reverse('api-applications-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)


    def test_application_create_wrong_resume_owner(self):
        other_student = User.objects.create_user(username='other_student', password='pass')
        other_resume = Resume.objects.create(user=other_student, title='Other CV', content='...')

        self.client.force_authenticate(user=self.student)
        url = reverse('api-jobs-apply', kwargs={'pk': self.job.pk})
        data = {
            'resume': other_resume.pk,
            'cover_letter': 'Пытаюсь использовать чужое резюме'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Заявка не должна создаться
        self.assertEqual(Application.objects.count(), 0)

    def test_job_list_fields(self):
        url = reverse('api-jobs-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data[0]
        self.assertIn('id', data)
        self.assertIn('title', data)
        self.assertIn('description', data)
        self.assertIn('employer', data)
        self.assertIn('remote', data)
        self.assertEqual(data['title'], self.job.title)
        self.assertEqual(data['remote'], True)

    def test_application_list_isolation(self):
        other_student = User.objects.create_user(username='intruder', password='pass')
        Application.objects.create(
            job=self.job,
            user=other_student,
            resume=Resume.objects.create(user=other_student, title='Intruder CV', content='...'),
            cover_letter='Чужой отклик'
        )
        Application.objects.create(
            job=self.job,
            user=self.student,
            resume=self.student_resume,
            cover_letter='Мой отклик'
        )

        self.client.force_authenticate(user=self.student)
        url = reverse('api-applications-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # видит только свою
        self.assertEqual(response.data[0]['user'], self.student.id)

    def test_application_create_nonexistent_job(self):
        self.client.force_authenticate(user=self.student)
        url = reverse('api-jobs-apply', kwargs={'pk': 99999})  # несуществующий pk
        data = {
            'resume': self.student_resume.pk,
            'cover_letter': 'Хочу на несуществующую работу'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_application_create_empty_cover_letter(self):
        self.client.force_authenticate(user=self.student)
        url = reverse('api-jobs-apply', kwargs={'pk': self.job.pk})
        data = {
            'resume': self.student_resume.pk,
            'cover_letter': ''
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Application.objects.count(), 1)
        self.assertEqual(Application.objects.first().cover_letter, '')