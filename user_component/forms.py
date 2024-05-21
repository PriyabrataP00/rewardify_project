from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from user_component.models import Screenshot


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required= True, help_text='First Name')
    last_name = forms.CharField(max_length=30, required= True, help_text='Last Name')
    email = forms.EmailField(max_length=254, required= True, help_text='Email Address')

    class Meta:
        model = User
        fields =('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class ScreenshotUploadForm(forms.ModelForm):
    class Meta:
        model = Screenshot
        fields = ['image']

class ProfileUpdateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
