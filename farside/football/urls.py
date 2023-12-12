from django.urls import path
from . import views

app_name = 'football'

urlpatterns = [
    path('', views.football_index, name='football_index'),
    path('add_team', views.add_team, name='add_team'),
    path('pick_game', views.pick_game, name='pick_game'),
    path('season/<int:year>/week/<int:week>/', views.pick_week, name='pick_week'),
    path('results/', views.result_list, name='result_list'),
    path('results/<int:year>/', views.result_year, name='result_year'),
    path('results/<int:year>/week/<int:week>/', views.result_week, name='result_week')
] 