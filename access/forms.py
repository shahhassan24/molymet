from django import forms
from django.forms import ModelForm
from .models import User

class LoginForm(forms.Form):
	username = forms.CharField(max_length=65)
	password = forms.CharField(max_length=65, widget=forms.PasswordInput)

class SecondFactorForm(forms.Form):
	second_factor = forms.CharField(max_length=10)

class ResetForm(forms.Form):
	email = forms.EmailField()

