from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import *
from .models import *
import datetime

# Create your views here.

def index(request):
  
  return render(request, 'index.html', context={})

def add_team(request):
  if request.method == 'POST':
    form = TeamForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect(reverse('football:index'))
  else:
    form = TeamForm()
      
  return render(request, 'add_team.html', context={'form':form})

def pick_game(request):
  games_list = Game.objects.all()
  
  if request.method == 'POST':
    form = PickForm(request.POST)
    if form.is_valid():
      print(True)
      print(form.cleaned_data)
      pick = form.save(commit=False)
      # pick.user = request.user
      user_save = User.objects.get(id=1)
      pick.user = user_save
      pick.submit_date = datetime.datetime.now()
      pick.save()
      return redirect(reverse('football:index'))
  else:
    form = PickForm()
    
  return render(request, 'pick_game.html', context={'form':form, 'games_list': games_list})
