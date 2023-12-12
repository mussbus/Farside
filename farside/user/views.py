from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import *

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            return redirect('football:index')
    else:
        form = RegisterForm()    
  
    return render(request, 'register.html', {'form':form})