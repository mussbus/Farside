from django.db import models
from django.core.validators import *
from django.contrib.auth.models import User 
import datetime

# Create your models here.

class Conference(models.Model):
  conference_id = models.BigAutoField(primary_key=True)
  name = models.CharField(validators=[MaxLengthValidator(30)], max_length=30)
  abbreviation = models.CharField(validators=[MaxLengthValidator(3), MinLengthValidator(3)], max_length=3)
  
  def __str__(self):
    return f"{self.abbreviation}"
  
  class Meta:
    ordering = ['abbreviation']

class Division(models.Model):
  division_id = models.BigAutoField(primary_key=True)
  name = models.CharField(validators=[MaxLengthValidator(5)], max_length=5)
  conference = models.ForeignKey('Conference', on_delete=models.CASCADE)  
  
  def __str__(self):
    return f"{self.conference.abbreviation} {self.name}"
  
  class Meta:
    ordering = ['conference', 'name']
    
class Team(models.Model):
  team_id = models.BigAutoField(primary_key=True)
  abbreviation = models.CharField(validators=[MaxLengthValidator(3), MinLengthValidator(3)], max_length=3)
  location = models.CharField(validators=[MaxLengthValidator(30)], max_length=30)
  name = models.CharField(validators=[MaxLengthValidator(30)], max_length=30)
  division = models.ForeignKey('Division', on_delete=models.CASCADE)
  
  def __str__(self):
    return f"{self.location} {self.name} ({self.abbreviation})"
  
  class Meta:
    ordering = ['location', 'name']
  
class Week(models.Model):
  week_id = models.BigAutoField(primary_key=True)
  week = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(18)])
  season = models.ForeignKey('Season', on_delete=models.CASCADE)
  time_start = models.DateTimeField()
  time_end = models.DateTimeField()
  
  def __str__(self):
    return f"{self.season.year} Season, Week {self.week}"
  
  class Meta:
    ordering = ['season', 'week']
  
class Season(models.Model):
  season_id = models.BigAutoField(primary_key=True)
  year = models.IntegerField(validators=[MinValueValidator(2018)])
  
  def __str__(self):
    return f"{self.year} Season"
  
  class Meta:
    ordering = ['year']
  
class Pick(models.Model):
  pick_id = models.BigAutoField(primary_key=True)
  value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(16)], null=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
  week = models.ForeignKey('Week', on_delete=models.CASCADE, null=True)
  team = models.ForeignKey('Team', on_delete=models.CASCADE, null=True)
  game = models.ForeignKey('Game', on_delete=models.CASCADE, null=True)
  submit_date = models.DateTimeField(default=datetime.datetime.now())
  
  def __str__(self):
    return f"{self.user.first_name}{self.user.last_name} put {self.value} on the {self.team.location} {self.team.name} to win in Week {self.week.week}"
  
  
class Game(models.Model):
  game_id = models.BigAutoField(primary_key=True)
  start_time = models.DateTimeField()
  away_score = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
  home_score = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
  week = models.ForeignKey('Week', on_delete=models.CASCADE, null=True)  
  away_team = models.ForeignKey('Team', on_delete=models.CASCADE, null=True, related_name="Away_TeamID")
  home_team = models.ForeignKey('Team', on_delete=models.CASCADE, null=True, related_name="Home_TeamID")
  
  QUARTERS = (
    ('N', 'Not Started'),
    ('1', '1Q'),
    ('2', '2Q'),
    ('1', '3Q'),
    ('4', '4Q'),
    ('F', 'Finished')
  )
  
  game_status = models.CharField(max_length=1, choices=QUARTERS, blank=True, default='N')
  
  def __str__(self):
    return f"{self.week.season.year} Season Week {self.week.week} {self.away_team.abbreviation} at {self.home_team.abbreviation}"
  
  class Meta:
    ordering = ['week', 'start_time', 'game_id']
  
class Tiebreaker(models.Model):
  tiebreaker_id = models.BigAutoField(primary_key=True)
  tiebreaker_points = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(150)])
  submit_date = models.DateTimeField(default=datetime.datetime.now())
  week = models.ForeignKey('Week', on_delete=models.CASCADE, null=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
  game = models.ForeignKey('Game', on_delete=models.CASCADE, null=True)
  
  def __str__(self):
    return f"{self.user.first_name} {self.user.last_name} put {self.tiebreaker_points} as the tiebreaker on the {self.game.away_team.abbreviation} {self.game.home_team.abbreviation} game in Week {self.week.week}"
  
  class Meta:
    ordering: ['week.season', 'week.week', 'tiebreaker_points']