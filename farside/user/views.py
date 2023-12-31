from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .forms import *

# Create your views here.

def login_view(request):
    form = LoginForm(None)
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        username1 = request.POST.get('username')
        password1 = request.POST.get('password')
        user = form.get_user()
        
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('football:football_index')
            
    return render(request, 'login.html', {'form':form})

def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            return redirect('football:football_index')
  
    return render(request, 'register.html', {'form':form})