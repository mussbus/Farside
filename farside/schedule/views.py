from django.shortcuts import render, redirect
from .forms import *
import datetime
from football.models import *
from django.forms import *
from django.db.models import Count
# Create your views here.

def index(request):
    now = datetime.datetime.now()
    week_list = Week.objects.filter(time_end__gt=now).order_by('time_start')[:5]
    
    if request.method == 'POST':
        form_search = SearchWeekForm(request.POST)
        
        if form_search.is_valid():
            form_search_clean = form_search.cleaned_data
    
            if 'ADD_GAMES' in request.POST:
                return redirect(f'/schedule/add_games/season/{form_search_clean["season"]}/week/{form_search_clean["week"]}')
        
            if 'UPDATE_SCORES' in request.POST:
                form_update_scores = SearchWeekForm(request.POST)
                
                return redirect(f'/schedule/update_scores/season/{form_search_clean["season"]}/week/{form_search_clean["week"]}')
      
    else:
        form_update_scores = SearchWeekForm(None)  
        form_add_games = SearchWeekForm(None)  
  
    return render(request, 'schedule__index.html', context={'form_add_games': form_add_games, 
                                                          'form_update_scores': form_update_scores,
                                                          'week_list': week_list})

# ----------------------------------------------------------------------------------------------------------

def add_week_games(request, week, year):
    week = Week.objects.get(season__year=year, week=week)
    games_list = Game.objects.filter(week_id=week.week_id)
    games_formset = formset_factory(GameForm, extra=14, max_num=16, min_num=12)
    formset = games_formset(request.POST or None)
    
    if request.method == 'POST':                    
        if 'save' in request.POST:
            if formset.is_valid():
                for form in formset:
                    game = form.save(commit=False)
                    game.week = week
                    game.save()
                    
                return redirect(f'/schedule/edit_games/season/{year}/week/{week.week}')
            
    else:    
        if len(games_list) > 0:
            return redirect(f'/schedule/edit_games/season/{year}/week/{week.week}')
        
    return render(request, 'add_week_games.html', context={'formset': formset})

# ----------------------------------------------------------------------------------------------------------

def edit_week_games(request, week, year):
    delete = False
    edit = False
    game_id = -1
    game_form = GameForm(None)
    
    if request.method == 'POST':
        if 'add' in request.POST:
            edit = True
            
        if 'edit' in request.POST:
            game_id = int(request.POST['edit'])
            game_obj = Game.objects.get(game_id=game_id)
            game_form = GameForm(None, instance=game_obj)
            edit = True
        
        elif 'save' in request.POST:
            edit = True
            game_id = int(request.POST['save'])
            game_obj = Game.objects.get(game_id=game_id)
            game_form = GameForm(request.POST, instance=game_obj)
            if game_form.is_valid:
                game_form.save()
                edit = False
            
        elif 'delete' in request.POST:
            game_id = int(request.POST['delete'])
            delete = True
            
        elif 'confirm_delete' in request.POST:
            game_id = int(request.POST['confirm_delete'])
            Game.objects.filter(pk=game_id).delete()
            game_id = -1
    
    obj_week = Week.objects.get(season__year=year, week=week)
    games_list = Game.objects.filter(week_id=obj_week.week_id) 
        
    return render(request, 'edit_week_games.html', context={
        'games_list':games_list, 
        'game_form': game_form,
        'delete': delete,
        'edit': edit,
        'game_id': game_id,
        'week': week})

# ----------------------------------------------------------------------------------------------------------

def update_week_scores(request, week, year):
    obj_week = Week.objects.get(season__year=year, week=week)
    games_list = Game.objects.filter(week=obj_week).order_by('game_time__day__add_days', 'game_time__game_time', 'game_id')
    update_scores_formset = formset_factory(form=ScoreForm, formset=ScoreFormset, extra=len(games_list))
    formset = update_scores_formset(request.POST or None)
    
    length_games = len(formset.forms)
    
    for game, form in zip(games_list, formset):
        form.fields['away_score'].initial = game.away_score
        form.fields['home_score'].initial = game.home_score
        form.fields['game_status'].initial = game.game_status
        form.fields['away_score'].label = f'{game.away_team.location} {game.away_team.name}'
        form.fields['home_score'].label = f'{game.home_team.location} {game.home_team.name}'
        form.fields['game_status'].label = 'Game Status'
        
    
    if request.method == 'POST':
        if formset.is_valid():
            for game, form in zip(games_list, formset):
                clean_form = form.cleaned_data
                game.away_score = clean_form['away_score']
                game.home_score = clean_form['home_score']
                game.game_status = clean_form['game_status']
                game.save()
                
            calculate_week_scores(obj_week, games_list)
                
    games_formset = zip(games_list, formset)
    
    return render(request, 'update_week_scores.html', context={'games_formset': games_formset,
                                                               'formset': formset,
                                                               'games_list': games_list})

# ----------------------------------------------------------------------------------------------------------

def calculate_week_scores(obj_week, games_list):
    number_of_games = len(games_list)
    number_of_teams = number_of_games * 2  
    team_id_matrix = [0] * number_of_teams
    team_name_matrix = [''] * number_of_teams
    win_matrix = [0] * number_of_teams
    
    # Caclulates matrix used to multiply scores
    for game_number, game in enumerate(games_list):
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
            
    # get picks, number of users
    pick_list = Pick.objects.filter(week=obj_week).order_by('user__id', 'game__game_time__day__add_days', 'game__game_time__game_time', 'game__game_id').select_related('user', 'week', 'team', 'game')  
    user_count = Pick.objects.filter(week=obj_week).values('user_id').annotate(count=Count('user_id'))
    total_users = len(user_count)  
    pick_matrix = []
    user_matrix = []
    sum_matrix = [0] * total_users
    
    # add all users to user list
    for user in user_count:
        user_matrix.append(user['user_id'])
  
    # get all picks for a given team, check if user picked that team, 
    # check if team won, then add that to user's total
    for team_index, team in enumerate(team_id_matrix):
        team_picks = pick_list.filter(team__team_id=team).order_by('user__id')
        team_pick_list = [0] * total_users
    
        if win_matrix[team_index] > 0:
            for index, user in enumerate(user_matrix):
                user_pick = team_picks.filter(user__id=user)
            
                if not user_pick:
                    team_pick_list[index] = 0
                else:
                    team_pick_list[index] = user_pick[0].value        
                
                sum_matrix[index] += win_matrix[team_index] * team_pick_list[index]  
                pick_matrix.append(team_pick_list)
    
    # save total
    for user, total_points in zip(user_matrix, sum_matrix):
        try:
            obj_total = Total.objects.get(week=obj_week, user__id=user)
        except:
            obj_total = Total()
        
        obj_user = User.objects.get(id=user)
        
        try:
            obj_tiebreaker = Tiebreaker.objects.get(week=obj_week, user__id=user)
        except:
            obj_tiebreaker = Tiebreaker()
            obj_tiebreaker.points = 0
            obj_tiebreaker.user = obj_user
            obj_tiebreaker.week = obj_week
        
            
        obj_total.week = obj_week
        obj_total.user = obj_user
        obj_total.total = total_points
        obj_total.tiebreaker = obj_tiebreaker
        obj_total.save()
        
    return