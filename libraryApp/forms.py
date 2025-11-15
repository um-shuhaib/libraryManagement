from django.contrib.auth.forms import UserCreationForm
from libraryApp.models import User
from django import forms

class UserRegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields=["first_name","username","email","password1","password2","phone","profile"]

        widgets={
            'first_name':forms.TextInput(attrs={'class':'form-control','id':'inputFirstName'}),
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'password1':forms.PasswordInput(attrs={'class':'form-control'}),
            'password2':forms.PasswordInput(attrs={'class':'form-control'}),
            'phone':forms.TextInput(attrs={'class':'form-control'}),
            'profile':forms.FileInput(attrs={'class':'form-control'}),
        }
    # Override password fields to add class
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )