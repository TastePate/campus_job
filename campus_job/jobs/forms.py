from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile, Job, Resume, Employer

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Логин",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '',
            'autofocus': True
        })
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': ''
        })
    )

class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': ''}),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': ''}),
    )
    password2 = forms.CharField(
        label="Подтвердите пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': ''}),
    )
    role = forms.ChoiceField(
        choices=Profile.ROLE_CHOICES,
        label="Я регистрируюсь как",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                role=self.cleaned_data['role']
            )
        return user

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'title', 'description', 'category', 'job_type',
            'remote', 'location', 'slots', 'expires_at'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название вакансии'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Опишите вакансию...'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'job_type': forms.Select(attrs={'class': 'form-select'}),
            'remote': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Здание, кабинет или адрес'}),
            'slots': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'expires_at': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'title': 'Название вакансии',
            'description': 'Описание',
            'category': 'Категория',
            'job_type': 'Тип занятости',
            'remote': 'Удалённая работа',
            'location': 'Локация',
            'slots': 'Количество мест',
            'expires_at': 'Дата окончания приёма заявок',
        }


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: Junior Python Developer'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 15,
                'placeholder': 'Опишите ваш опыт, навыки, образование...'
            }),
        }
        labels = {
            'title': 'Заголовок резюме',
            'content': 'Содержание резюме',
        }


class EmployerForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ['org_name', 'description', 'department']
        widgets = {
            'org_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название вашей организации'}),
            'description': forms.Textarea(attrs={'rows': 5, 'class': 'form-control', 'placeholder': 'Расскажите о компании, ценностях, команде...'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'org_name': 'Название организации',
            'description': 'Описание',
            'department': 'Кафедра / Подразделение',
        }