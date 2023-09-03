from django.urls import path
from . import views

app_name = 'football'

urlpatterns = [
  path('', views.index, name='index'),
  path('add_team', views.add_team, name='add_team'),
  path('pick_game', views.pick_game, name='pick_game'),
  path('season/<int:year>/week/<int:week>/', views.pick_week, name='pick_week'),
  path('test_formset', views.test_formset, name='test_formset')
] 