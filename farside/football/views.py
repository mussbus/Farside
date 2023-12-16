from django.shortcuts import render, redirect
from django.urls import reverse
from django.forms.formsets import formset_factory
from django.db.models import Count, Sum
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
import datetime
import random
from schedule.views import calculate_week_scores

# Create your views here.

def football_index(request):  
    return render(request, 'football_index.html', context={})

# ----------------------------------------------------------------------------------------------------------

def add_team(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('football:index'))
    else:
        form = TeamForm()
      
    return render(request, 'add_team.html', context={'form':form})

# ----------------------------------------------------------------------------------------------------------

def pick_game(request):
    games_list = Game.objects.filter(game_id = 1)
  
    if request.method == 'POST':
        form = PickForm(request.POST)
    
        if form.is_valid():
            print(True)
            print(form.cleaned_data)
            pick = form.save(commit=False)
            pick.user = request.user
            pick.submit_date = datetime.datetime.now()
            pick.save()
            return redirect(f'/football/season/{year}/week/{week}')
    
    else:
        form = PickForm()
    
    return render(request, 'pick_game.html', context={'form':form, 'games_list': games_list})

# ----------------------------------------------------------------------------------------------------------

def pick_week(request, year, week):
    week = Week.objects.get(season__year=year, week=week)
    games_list = Game.objects.filter(week_id=week.week_id)
    picks_list = Pick.objects.filter(week_id=week.week_id, user_id=request.user)
    number_of_games = len(games_list)
    pick_formset = formset_factory(PickForm, extra=number_of_games)
    formset = pick_formset(request.POST or None)
    try:
        tiebreaker_object = Tiebreaker.objects.get(week_id=week.week_id, user_id=request.user)
    except Tiebreaker.DoesNotExist:
        tiebreaker_object = None
    
    PICK_OPTIONS = [('-1', '---')]
    count = 1
  
    while count <= number_of_games:
        PICK_OPTIONS += [(f'{count}', f'{count}')]
        count += 1
  
    for game, form in zip(games_list, formset):
        form.fields['home_team_points'].choices = PICK_OPTIONS
        form.fields['away_team_points'].choices = PICK_OPTIONS
        form.fields['home_team_points'].label = f'{game.home_team.location} {game.home_team.name}'
        form.fields['away_team_points'].label = f'{game.away_team.location} {game.away_team.name}'
        form.fields['game_id'].initial = game.game_id
        form.fields['home_team_id'].initial = game.home_team.team_id
        form.fields['away_team_id'].initial = game.away_team.team_id
        
        for pick in picks_list:
            if pick.game.game_id == game.game_id:
                if pick.team.team_id == game.away_team.team_id:
                    form.fields['away_team_points'].initial = f'{pick.value}'
                else:
                    form.fields['home_team_points'].initial = f'{pick.value}'
                    
                form.fields['pick_id'].initial = pick.pick_id
            
    if request.method == 'POST':       
        form_tiebreaker = TiebreakerForm(request.POST, instance=tiebreaker_object)
        
        if all([formset.is_valid(), form_tiebreaker.is_valid]):
            for form in formset:
                pick_form = form.cleaned_data                
                game_id = pick_form['game_id']
                
                pick = Pick()
                
                if pick_form['pick_id'] > 0:
                    pick.pick_id = pick_form['pick_id']
                    
                pick.user = request.user
                pick.submit_date = datetime.datetime.now()
                pick.game = Game.objects.get(game_id=game_id)
                pick.week = week
                
                if int(pick_form['away_team_points']) > 0:
                    team_id = pick_form['away_team_id']                
                    pick.value = pick_form['away_team_points']
                    pick.team = Team.objects.get(team_id=team_id)
                else:
                    team_id = pick_form['home_team_id']                
                    pick.value = pick_form['home_team_points']
                    pick.team = Team.objects.get(team_id=team_id)
                
                pick.save()
            
            tiebreaker = form_tiebreaker.save(commit=False)
            tiebreaker.user = request.user
            tiebreaker.game = games_list.last()
            tiebreaker.week = week
            tiebreaker.submit_date = datetime.datetime.now()
            tiebreaker.save()
            
            url_is = request.build_absolute_uri()
            return redirect(reverse('football:index'))
    else:
        form_tiebreaker = TiebreakerForm(None, instance=tiebreaker_object)
      
    game_form = zip(games_list, formset)
    
    
    
    return render(request, 'pick_week.html', context={'game_form': game_form, 
                                                        'form_tiebreaker': form_tiebreaker,
                                                        'formset': formset})

# ----------------------------------------------------------------------------------------------------------

def result_list(request):
    season_list = Season.objects.order_by('year')
  
    return render(request, 'results_list.html', context={'season_list': season_list})

# ----------------------------------------------------------------------------------------------------------

def result_year(request, year):
    season = Season.objects.get(year=year)
    week_list = Week.objects.filter(season=season.season_id)
    print(week_list)
    
    return render(request, 'results_year.html', context={'week_list': week_list})

# ----------------------------------------------------------------------------------------------------------
@login_required
def result_week(request, year, week):
    week = Week.objects.get(season__year=year, week=week)
    qs_total_week = Total.objects.filter(week=week).order_by('-total')
    qs_total_season = Total.objects.values('user__id').filter(week__season__year=year, week__week__lte=week.week).annotate(total_season=Sum('total')).order_by('-total_season')
    qs_game = Game.objects.order_by_time(week.week_id)
    
    list_user = list()
    list_picks = list()
    list_teams = list()    
    dict_season_rank = dict()
        
    for index, q_total_season in enumerate(qs_total_season):
        user_rank = dict()
        user_rank['season_rank'] = index + 1
        user_rank['season_total'] = q_total_season['total_season']
        dict_season_rank[q_total_season['user__id']] = user_rank
        
    index = 1
    
    for total in qs_total_week:
        obj_user = dict()
        obj_user['id']= total.user_id
        obj_user['name'] = total.user.first_name + ' ' + total.user.last_name[0]
        obj_user['season_total'] = dict_season_rank.get(total.user_id).get('season_total')
        obj_user['season_rank'] = dict_season_rank.get(total.user_id).get('season_rank')
        obj_user['week_total'] = total.total
        obj_user['week_rank'] = index
        list_user.append(obj_user)
        
        index = index + 1
        
    for game in qs_game:
        obj_away_team = dict()
        obj_home_team = dict()
        
        obj_away_team['name'] = game.away_team.full_name + ' at'
        obj_away_team['score'] = game.away_score;
        
        obj_home_team['name'] = game.home_team.full_name
        obj_home_team['score'] = game.home_score;
        
        if game.away_score > game.home_score:
            obj_away_team['result'] = 'win'
            obj_home_team['result'] = 'loss'
        elif game.away_score < game.home_score:
            obj_away_team['result'] = 'loss'
            obj_home_team['result'] = 'win'
        else:
            obj_away_team['result'] = 'tie'
            obj_home_team['result'] = 'tie'
        
        list_teams.append(obj_away_team)
        list_teams.append(obj_home_team)
        
        qs_away_picks = Pick.objects.filter(week=week, team=game.away_team).select_related('user')
        qs_home_picks = Pick.objects.filter(week=week, team=game.home_team).select_related('user')
        
        list_away_pick = list()
        list_home_pick = list()
        
        for user in list_user:            
            try:
                q_away_pick = qs_away_picks.get(user__id=user['id'])
                list_away_pick.append(q_away_pick.value)
            except:
                list_away_pick.append(' ')
                
            try:
                q_home_pick = qs_home_picks.get(user__id=user['id'])
                list_home_pick.append(q_home_pick.value)
            except:
                list_home_pick.append(' ')
                
        list_picks.append(list_away_pick) 
        list_picks.append(list_home_pick)
        
    list_info = zip(list_teams, list_picks)
    
    # if request.method == 'POST': 
    #     make_test_results()
  
    return render(request, 'results_week.html', context={'list_user': list_user, 
                                                         'list_info': list_info})
  
# ----------------------------------------------------------------------------------------------------------

def make_test_results():
    qs_week = Week.objects.filter(season__year=2022)
    
    length_of_week = len(qs_week)
    
    int_times = 1
    
    for q_week in qs_week:
        qs_game = Game.objects.filter(week=q_week)\
        
        calculate_week_scores(q_week, qs_game)
        
        int_times = int_times + 1
        
    # qs_user = User.objects.all()
    
    # list_pick = []
    # int_pick = 1
    # while int_pick < 17:
    #     list_pick.append(int_pick)
    #     int_pick = int_pick + 1
    
    # for q_week in qs_week:
    #     qs_game = Game.objects.filter(week=q_week).order_by('game_id')
        
    #     for q_user in qs_user:
    #         random.shuffle(list_pick)
            
    #         for index, q_game in enumerate(qs_game):
    #             int_pick_team = random.randint(0, 1)
                
    #             obj_pick = Pick()
    #             obj_pick.value = list_pick[index]
    #             obj_pick.user = q_user
    #             obj_pick.week = q_week
    #             obj_pick.game = q_game
                
    #             if int_pick_team == 0:
    #                 obj_pick.team = q_game.away_team
    #             else:
    #                 obj_pick.team = q_game.home_team
                    
    #             obj_pick.save()
                    
    #             if index == 15:
    #                 obj_tiebreaker = Tiebreaker()
    #                 obj_tiebreaker.tiebreaker_points = random.randint(25, 75)
    #                 obj_tiebreaker.week = q_week
    #                 obj_tiebreaker.game = q_game
    #                 obj_tiebreaker.user = q_user
    #                 obj_tiebreaker.save()
                    
    #                 letterman = 1234
    
    return

    # q_season = Season.objects.get(year=2022)
    # date = datetime.datetime(2022, 9, 6)
    
    # for x in range(1, 18):
    #     obj_week = Week()
    #     obj_week.season = q_season
    #     obj_week.week = x
    #     obj_week.time_start = date
    #     date = date + datetime.timedelta(days=7)
    #     obj_week.time_end = date
    #     obj_week.save()   
    
    
    # list_first_name = get_first_name()
    # list_last_name = get_last_name()
    
#     for i in range (5, 31):
#         user = User()
#         user.username = list_first_name[i - 5] + '_' + list_last_name[i - 5]
#         user.first_name = list_first_name[i - 5]
#         user.last_name = list_last_name[i - 5]
#         user.email = list_first_name[i - 5] + '_' + list_last_name[i - 5] + '@gmail.com'
#         user.active = True
#         user.password = 'Chad123!'
#         user.save()
    
# def get_first_name():
#     list_name = list()
    
#     list_name.append('Ryan')
#     list_name.append('Emily')
#     list_name.append('Megan')
#     list_name.append('Olivia')
#     list_name.append('Ellie')
#     list_name.append('Mark')
#     list_name.append('Miles')
#     list_name.append('Shannon')
#     list_name.append('Luke')
#     list_name.append('Evan')
#     list_name.append('Courtney')
#     list_name.append('Ella')
#     list_name.append('Cali')
#     list_name.append('Elizabeth')
#     list_name.append('Brian')
#     list_name.append('Zach')
#     list_name.append('Wes')
#     list_name.append('Lauren')
#     list_name.append('Mia')
#     list_name.append('Mike')
#     list_name.append('Achilles')
#     list_name.append('Odysseus')
#     list_name.append('Zeus')
#     list_name.append('Zeke')
#     list_name.append('Gabbie')
#     list_name.append('Lana')
    
#     return list_name

# def get_last_name():
#     list_name = list()
    
#     list_name.append('Johnson')
#     list_name.append('Munson')
#     list_name.append('Birch')
#     list_name.append('Schneider')
#     list_name.append('Hilda')
#     list_name.append('Muth')
#     list_name.append('Machado')
#     list_name.append('Harper')
#     list_name.append('Mulch')
#     list_name.append('Mahomes')
#     list_name.append('Mac')
#     list_name.append('Johnson')
#     list_name.append('Washington')
#     list_name.append('Miller')
#     list_name.append('Hollins')
#     list_name.append('Rivers')
#     list_name.append('James')
#     list_name.append('Iverson')
#     list_name.append('Barber')
#     list_name.append('Deville')
#     list_name.append('Jaemes')
#     list_name.append('Homa')
#     list_name.append('Johnson')
#     list_name.append('Musso')
#     list_name.append('Karter')
#     list_name.append('Streets')
    
#     return list_name
  
  
  
    #   qs_team = Team.objects.all()
    # qs_week = Week.objects.filter(season__year=2022)
    # list_team = []
    # num_games = len(qs_team) / 2
  
  
  # for team in qs_team:
    #     list_team.append(team.team_id)
        
        
    # for week in qs_week:
    #     random.shuffle(list_team)
        
        # game_number = 0
        
        # while game_number < 16:
        #     away_team_number = list_team[game_number * 2]
        #     home_team_number = list_team[game_number * 2 + 1]
            
            
        #     obj_game = Game()
        #     obj_game.game_status = 'F'
        #     obj_game.away_team = qs_team.get(team_id=away_team_number)
        #     obj_game.home_team = qs_team.get(team_id=home_team_number)
        #     obj_game.away_score = random.randint(0, 50)
        #     obj_game.home_score = random.randint(0, 50)
        #     obj_game.week = week
        #     obj_game.game_time = GameTime.objects.get(game_time_id=4)
        #     obj_game.save()
            
        #     game_number = game_number + 1