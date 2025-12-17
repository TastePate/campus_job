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
            'description': forms.Textarea(attrs={'rows': 5}),
            'expires_at': forms.DateInput(attrs={'type': 'date'}),
        }


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Например: Junior Python Developer'}),
            'content': forms.Textarea(attrs={'rows': 15, 'placeholder': 'Опишите ваш опыт, навыки, образование...'}),
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