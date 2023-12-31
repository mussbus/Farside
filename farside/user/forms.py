from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.forms import ModelForm

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'class': 'input__login', 'autofocus': True}))
    password = forms.CharField(strip=False,
                               widget=forms.PasswordInput(attrs={'class': 'input__login', 'autocomplete': 'current-password'}))
    

class RegisterForm(ModelForm):
    password2 = forms.CharField(label='Confirm Password', label_suffix=':',
        widget=forms.PasswordInput(attrs={'class': 'input__login'}))    
    
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email'
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input__login', 'autocomplete': 'new-password'}),
            'password': forms.PasswordInput(attrs={'class': 'input__login', 'autocomplete': 'new-password'}),
            'email': forms.EmailInput(attrs={'class': 'input__login'}),
            'first_name': forms.TextInput(attrs={'class': 'input__login'}),
            'last_name': forms.TextInput(attrs={'class': 'input__login'}),
        }
        
    field_order = ['username', 'password', 'password2', 'email', 'first_name', 'last_name']
    
    def clean(self):
        form_data = self.cleaned_data
        if form_data['password'] != form_data['password2']:
            raise forms.ValidationError('Both passwords must match')
            
        return form_data