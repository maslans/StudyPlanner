from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Task, Subject, StudentProfile, University, FieldOfStudy
from django.core.exceptions import ValidationError
from datetime import date

class UserWithProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    birthdate = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    school = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    field_of_study = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        profile_instance = kwargs.pop('profile_instance', None)
        super().__init__(*args, **kwargs)
        if profile_instance:
            self.fields['birthdate'].initial = profile_instance.birthdate
            self.fields['school'].initial = profile_instance.school
            self.fields['field_of_study'].initial = profile_instance.field_of_study

    def save(self, user_instance, commit=True):
        user = super().save(commit=commit)

        profile = StudentProfile.objects.get(user=user_instance)
        profile.birthdate = self.cleaned_data['birthdate']
        
        profile.school, created = University.objects.get_or_create(
            name=self.cleaned_data['school']
        )

        profile.field_of_study, created = FieldOfStudy.objects.get_or_create(
            name=self.cleaned_data['field_of_study'],
            university = profile.school
        )

        if commit:
            profile.save()
        return user

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True, max_length=150)
    last_name = forms.CharField(required=True, max_length=150)   
    birthdate = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    school = forms.CharField(max_length=255, required=True)
    field_of_study = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'birthdate', 'school', 'field_of_study']

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['school', 'field_of_study', 'birthdate']
        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
        }

class TaskForm(forms.ModelForm):
     def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')

        if self.instance and self.instance.pk:
            return due_date

        if due_date < date.today():
            raise ValidationError("The date cannot be later than today.")
        return due_date
     
     class Meta:
        model = Task
        fields = ['subject','title', 'description', 'due_date']

        widgets = {
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'due_date': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),
            'is_done': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name']
