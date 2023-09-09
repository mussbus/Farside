from django.shortcuts import render, redirect
from django.urls import reverse
from django.forms import formset_factory
from django.db.models import Count
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
      return redirect(f'/football/season/{year}/week/{week}')
  else:
    form = PickForm()
    
  return render(request, 'pick_game.html', context={'form':form, 'games_list': games_list})



def pick_week(request, year, week):
  # season = Season.objects.get(year=year)
  week = Week.objects.get(season__year=year, week=week)
  games_list = Game.objects.filter(week_id=week.week_id)
  number_of_extra_forms = len(games_list)
  formset = formset_factory(PickForm, extra=number_of_extra_forms)
  
  if request.method == 'POST':
    formset_post = formset(request.POST)
    form_tiebreaker_post = TiebreakerForm(request.POST)
    if formset_post.is_valid():
      for form in formset_post:
        pick = form.save(commit=False)
        pick.user = request.user
        pick.submit_date = datetime.datetime.now()
        pick.save()
    if form_tiebreaker_post.is_valid():
      tiebreaker = form_tiebreaker_post.save(commit=False)
      tiebreaker.user = request.user
      tiebreaker.game = games_list.last()
      tiebreaker.week = games_list.last().week
      tiebreaker.submit_date = datetime.datetime.now()
      tiebreaker.save()
      
    return redirect(reverse('football:pick_week'))
  
  else:
    form_tiebreaker = TiebreakerForm()
    
  return render(request, 'pick_week.html', context={'formset':formset, 
                                                    'games_list': games_list, 
                                                    'form_tiebreaker': form_tiebreaker})



def result_list(request):
  season_list = Season.objects.order_by('year')
  
  return render(request, 'results_list.html', context={'season_list': season_list})



def result_year(request, year):
  season = Season.objects.get(year=year)
  week_list = Week.objects.filter(season=season.season_id)
  print(week_list)
  
  return render(request, 'results_year.html', context={'week_list': week_list})



def result_week(request, year, week):  
  week = Week.objects.get(season__year=year, week=week)
  game_list = Game.objects.filter(week=week).order_by('start_time', 'game_id')  
  number_of_games = len(game_list)
  number_of_teams = number_of_games * 2  
  team_id_matrix = [0] * number_of_teams
  team_name_matrix = [''] * number_of_teams
  win_matrix = [0] * number_of_teams
  
  # Caclulates matrix used to multiply scores
  for game_number, game in enumerate(game_list):
    away_index = game_number * 2
    home_index = game_number * 2 + 1
    if game.game_status == 'F':
      if game.away_score > game.home_score:
        win_matrix[away_index] = 1
      else:
        win_matrix[home_index] = 1
        
      team_id_matrix[away_index] = game.away_team.team_id
      team_id_matrix[home_index] = game.home_team.team_id      
      team_name_matrix[away_index] = f'{game.away_team.location} {game.away_team.name}'
      team_name_matrix[home_index] = f'{game.home_team.location} {game.home_team.name}'
      
  pick_list = Pick.objects.filter(week__week=week.week_id).order_by('user__id', 'game__start_time', 'game__game_id').select_related('user', 'week', 'team', 'game')  
  user_count = Pick.objects.filter(week__week=week.week_id).values('user_id').annotate(count=Count('user_id'))
  total_users = len(user_count)  
  pick_matrix = []
  user_matrix = []
  sum_matrix = [0] * total_users
  
  for user in user_count:
    user_matrix.append(user['user_id'])
  
  for team_index, team in enumerate(team_id_matrix):
    team_picks = pick_list.filter(team__team_id=team).order_by('user__id')
    team_pick_list = [0] * total_users
    
    for index, user in enumerate(user_matrix):
      user_pick = team_picks.filter(user__id=user)
      
      if not user_pick:
        team_pick_list[index] = 0
      else:
        team_pick_list[index] = user_pick[0].value        
          
      sum_matrix[index] += win_matrix[team_index] * team_pick_list[index]
  
    pick_matrix.append(team_pick_list)
  
  table_row_matrix = zip(team_name_matrix, win_matrix, pick_matrix)
  
  return render(request, 'results_week.html', context={'table_row_matrix':table_row_matrix, 
                                                       'sum_matrix':sum_matrix})
  