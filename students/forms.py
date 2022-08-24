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