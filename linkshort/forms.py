from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import EmailValidator
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label='',
        max_length=150,
        min_length=5,
        widget=forms.TextInput(attrs={'class': 'form-control bg-light mb-3', 'placeholder': 'Enter Username'})
    )
    
    email = forms.CharField(
        label='',
        max_length=100,
        min_length=10,
        validators=[EmailValidator()],
        widget=forms.EmailInput(attrs={'class': 'form-control bg-light mb-3', 'placeholder': 'Enter Email'})
    )

    password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'class': 'form-control bg-light mb-3', 'placeholder': 'Enter Password'})
    )
    
    password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'class': 'form-control bg-light mb-3', 'placeholder': 'Confirm Password'})
    )
    
    usable_password = None

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
        
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='',
        max_length=150,
        min_length=5,
        widget=forms.TextInput(attrs={'class': 'form-control bg-light mb-3', 'placeholder': 'Enter Username'})
    )

    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'class': 'form-control bg-light mb-3', 'placeholder': 'Enter Password'})
    )

class URLForm(forms.Form):
    title = forms.CharField(
        label='',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control bg-light mb-3', 'placeholder': 'Enter Title'})
    )

    original_url = forms.URLField(
        label='', 
        widget=forms.URLInput(attrs={'class': 'form-control bg-light mb-3', 'placeholder': 'Enter the URL (including https://)'})
    )
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['title', 'link', 'shortlink']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control bg-light', 'placeholder': 'Title'}),
            'link': forms.URLInput(attrs={'class': 'form-control bg-light', 'placeholder': 'Original Link'}),
            'shortlink': forms.URLInput(attrs={'class': 'form-control bg-light', 'placeholder': 'Short Link', 'readonly': 'readonly'}),
        }