from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.contrib.auth.decorators import login_required
from football.models import *
from django.db.models import Count, Sum

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
            # set_user_session(request, user)
            return redirect(reverse('dashboard'))
            
    return render(request, 'login.html', {'form':form})

def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            return redirect('football:football_index')
  
    return render(request, 'register.html', {'form':form})

@login_required
def dashboard(request):
    current_week = request.session['current_week']
    current_year = request.session['current_year']
    q_week = Week.objects.get(week=current_week, season__year=current_year)
    
    # grab current week games    
    qs_games = Game.objects.order_by_time(q_week.week_id)
    
    # grab last week results
    if current_week > 1:
        qs_total_previous = Total.objects.filter(week__week=(current_week - 1), week__season__year=current_year).order_by('-total')
        list_total = list()
        int_total_length = len(qs_total_previous)
        int_user_index = -1
        
        for index, total in enumerate(qs_total_previous):
            if total.user == request.user:
                if index <= 3:
                    int_user_index = 1
                elif int_total_length - index <= 3:
                    int_user_index = int_total_length - index
                else:
                    int_user_index = index                    
                break
            
        qs_total_previous_display = qs_total_previous[int_user_index - 1 : int_user_index + 4]
        
        for index, total in enumerate(qs_total_previous_display):            
            dict_user_total = dict()
            dict_user_total['index'] = index + 1
            dict_user_total['name'] = total.user.get_full_name()
            dict_user_total['total'] = total.total
            list_total.append(dict_user_total)
                
        qs_total_season = Total.objects.values('user__id').filter(week__season__year=current_year, week__week__lte=current_week).annotate(total_season=Sum('total')).order_by('-total_season')
        qs_user = User.objects.all()        
        list_user = list()
        
        for index, total in enumerate(qs_total_season):
            obj_user = dict()
            obj_user['id']= total['user__id']
            obj_user['name'] = qs_user.get(id=total['user__id']).get_full_name()
            obj_user['season_total'] = total['total_season']
            obj_user['season_rank'] = index + 1
            list_user.append(obj_user)             
            
        qs_total = Total.objects.filter(week__season__year=current_year, week__week__lte=current_week)
        list_season_rank = list()
        index = 1
        dict_season_rank = dict()
        
        while index <= current_week:
            qs_week_total = qs_total_season.filter(week__week__lte=index)
            
            if index == 1:
                dict_season_rank['num_users'] = len(qs_week_total)
                
            for user_index, total in enumerate(qs_week_total):
                dict_season_week_rank = dict()
                
                if request.user.id == total['user__id']:
                    dict_season_week_rank['x'] = index
                    dict_season_week_rank['y'] = user_index + 1
                    list_season_rank.append(dict_season_week_rank)
                    
            index = index + 1
            
        dict_season_rank['list_season_rank'] = list_season_rank
    
    return render(request, 'dashboard.html', {'qs_games': qs_games,
                                              'list_total': list_total,
                                              'list_user': list_user,
                                              'dict_season_rank': dict_season_rank})

def set_user_session(request, user):
    current_week = request.session['current_week']
    current_year = request.session['current_year']
    q_week = Week.objects.get(week=current_week, season__year=current_year)
    
    # grab current week games    
    qs_games = Game.objects.order_by_time(q_week.week_id)
    
    if len(qs_games) > 0:
        request.session['current_week_games'] = list(qs_games)
    mammoth = 4
    