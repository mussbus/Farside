from django.urls import path
from . import views

app_name = 'schedule'

urlpatterns = [
  path('', views.index, name='index'),
  path('update_scores/season/<int:year>/week/<int:week>/', views.update_week_scores, name='update_week_scores'),
  path('add_games/season/<int:year>/week/<int:week>/', views.add_week_games, name='add_week_games'),
  path('edit_games/season/<int:year>/week/<int:week>/', views.edit_week_games, name='edit_week_games')
]