from django import forms
from .models import Student

class StudentLoginForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['email', 'password']
        labels = {
            'email': 'Email',
            'password': 'Password'
        }
        widgets = {
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'password': forms.PasswordInput(attrs={'class':'form-control'})
        }

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_number', 'first_name', 'last_name', 'email', 'password', 'current_year', 'field_of_study', 'gpa']
        labels = {
            'student_number': 'Student Number',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'password': 'Password',
            'current_year': 'Current Year',
            'field_of_study': 'Field of Study',
            'gpa': 'GPA'
        }
        widgets = {
            'student_number': forms.NumberInput(attrs={'class':'form-control'}), 
            'first_name': forms.TextInput(attrs={'class':'form-control'}), 
            'last_name': forms.TextInput(attrs={'class':'form-control'}), 
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'password': forms.PasswordInput(attrs={'class':'form-control'}),
            'current_year': forms.NumberInput(attrs={'class':'form-control'}),
            'field_of_study': forms.TextInput(attrs={'class':'form-control'}), 
            'gpa': forms.NumberInput(attrs={'class':'form-control'})
        }