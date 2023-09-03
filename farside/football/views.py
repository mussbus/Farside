from django.shortcuts import render, redirect
from django.urls import reverse
from django.forms import formset_factory
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
  games_list = Game.objects.filter(game_id = 1)
  
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

def pick_week(request, year, week):
  season = Season.objects.get(year=year)
  week = Week.objects.get(season=season.season_id, week=week)
  games_list = Game.objects.filter(week_id=week.week_id)
  # games_list = Game.objects.filter(week = 1).order_by('start_time', 'game_id')
  number_of_extra_forms = len(games_list)
  formset = formset_factory(PickForm, extra=number_of_extra_forms)
  
  if request.method == 'POST':
    formset_post = formset(request.POST)
    form_tiebreaker_post = TiebreakerForm(request.POST)
    if formset_post.is_valid():
      user_save = User.objects.get(id=1)
      for form in formset_post:
        pick = form.save(commit=False)
        # pick.user = request.user
        pick.user = user_save
        pick.submit_date = datetime.datetime.now()
        pick.save()
    if form_tiebreaker_post.is_valid():
      tiebreaker = form_tiebreaker_post.save(commit=False)
      tiebreaker.user = user_save
      # tiebreaker.game = Game.objects.get(game_id = 5)
      tiebreaker.game = games_list.last()
      tiebreaker.week = games_list.last().week
      tiebreaker.submit_date = datetime.datetime.now()
      tiebreaker.save()
    return redirect(reverse('football:pick_week'))
  else:
    form_tiebreaker = TiebreakerForm()
    
  return render(request, 'pick_week.html', context={'formset':formset, 'games_list': games_list, 'form_tiebreaker': form_tiebreaker})

def test_formset(request):
  games_list = Game.objects.filter(week = 1)
  number_of_extra_forms = len(games_list)
  week_games_formset = formset_factory(PickForm, extra=number_of_extra_forms)
  formset = week_games_formset
  return render(request, 'test_formset.html', context={'formset':formset})
  