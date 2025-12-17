from django import forms
from django.contrib.auth.models import User
from .models import Profile, Job, Resume, Employer


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def save(self):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
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