from django.db import models
from django.core.validators import *
from django.contrib.auth.models import User 

import datetime

# ----------------------------------------------------------------------------------------------------------

class Conference(models.Model):
  conference_id = models.BigAutoField(primary_key=True)
  name = models.CharField(validators=[MaxLengthValidator(30)], max_length=30)
  abbreviation = models.CharField(validators=[MaxLengthValidator(3), MinLengthValidator(3)], max_length=3)
  
  def __str__(self):
    return f"{self.abbreviation}"
  
  class Meta:
    ordering = ['abbreviation']

# ----------------------------------------------------------------------------------------------------------

class Division(models.Model):
  division_id = models.BigAutoField(primary_key=True)
  name = models.CharField(validators=[MaxLengthValidator(5)], max_length=5)
  conference = models.ForeignKey('Conference', on_delete=models.CASCADE)  
  
  def __str__(self):
    return f"{self.conference.abbreviation} {self.name}"
  
  class Meta:
    ordering = ['conference', 'name']
    
# ----------------------------------------------------------------------------------------------------------
    
class Team(models.Model):
    team_id = models.BigAutoField(primary_key=True)
    abbreviation = models.CharField(validators=[MaxLengthValidator(2), MinLengthValidator(3)], max_length=3)
    location = models.CharField(validators=[MaxLengthValidator(30)], max_length=30)
    name = models.CharField(validators=[MaxLengthValidator(30)], max_length=30)
    division = models.ForeignKey('Division', on_delete=models.CASCADE)
  
    def __str__(self):
        return f"{self.location} {self.name}"
  
    class Meta:
        ordering = ['location', 'name']
    
    @property
    def full_name(self):
        return f"{self.location} {self.name}"
    
  
# ----------------------------------------------------------------------------------------------------------
  
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
  
# ----------------------------------------------------------------------------------------------------------
  
class Season(models.Model):
  season_id = models.BigAutoField(primary_key=True)
  year = models.IntegerField(validators=[MinValueValidator(2018)])
  year_start = models.DateTimeField(default=datetime.datetime.now())
  year_end = models.DateTimeField(default=datetime.datetime.now())
  
  def __str__(self):
    return f"{self.year}"
  
  class Meta:
    ordering = ['year']
  
# ----------------------------------------------------------------------------------------------------------
  
class Pick(models.Model):
  pick_id = models.BigAutoField(primary_key=True)
  value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(16)], null=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
  week = models.ForeignKey('Week', on_delete=models.CASCADE, null=True)
  team = models.ForeignKey('Team', on_delete=models.CASCADE, null=True)
  game = models.ForeignKey('Game', on_delete=models.CASCADE, null=True)
  submit_date = models.DateTimeField(default=datetime.datetime.now())
  
  def __str__(self):
    return f"{self.user.first_name} {self.user.last_name} put {self.value} on the {self.team.location} {self.team.name} to win in Week {self.week.week}"
  
# ----------------------------------------------------------------------------------------------------------

class GameManager(models.Manager):
    def order_by_time(self, week_id):
      return self.filter(week__week_id=week_id).order_by('game_time__day__add_days', 'game_time__game_time', 'game_id')

class Game(models.Model):
  game_id = models.BigAutoField(primary_key=True)
  game_time = models.ForeignKey('GameTime', on_delete=models.CASCADE, null=True)
  away_score = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
  home_score = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
  week = models.ForeignKey('Week', on_delete=models.CASCADE, null=True)  
  away_team = models.ForeignKey('Team', on_delete=models.CASCADE, null=True, related_name="Away_TeamID")
  home_team = models.ForeignKey('Team', on_delete=models.CASCADE, null=True, related_name="Home_TeamID")
  
  STATUS = (
    ('', '---'),
    ('1', '1Q'),
    ('2', '2Q'),
    ('1', '3Q'),
    ('4', '4Q'),
    ('F', 'F')
  )
  
  game_status = models.CharField(max_length=1, choices=STATUS, blank=True, default='N')
  objects = GameManager()
  
  def __str__(self):
    return f"Week {self.week.week} {self.week.season.year} {self.away_team.abbreviation} at {self.home_team.abbreviation}"
  
#   class Meta:
#     ordering = ['week', 'game_time.day', 'game_time', 'game_id']
  
# ----------------------------------------------------------------------------------------------------------
  
class Tiebreaker(models.Model):
  tiebreaker_id = models.BigAutoField(primary_key=True)
  tiebreaker_points = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1000)])
  submit_date = models.DateTimeField(default=datetime.datetime.now())
  week = models.ForeignKey('Week', on_delete=models.CASCADE, null=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
  game = models.ForeignKey('Game', on_delete=models.CASCADE, null=True)
  
  def __str__(self):
    return f"{self.user.first_name} {self.user.last_name} put {self.tiebreaker_points} as the tiebreaker on the {self.game.away_team.abbreviation} {self.game.home_team.abbreviation} game in Week {self.week.week}"
  
  class Meta:
    ordering: ['week.season', 'week.week', 'tiebreaker_points']
  
# ----------------------------------------------------------------------------------------------------------
    
class Total(models.Model):
  total_id = models.BigAutoField(primary_key=True)
  total = models.IntegerField()
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
  week = models.ForeignKey('Week', on_delete=models.CASCADE, null=True)
  tiebreaker = models.ForeignKey('Tiebreaker', on_delete=models.CASCADE, null=True)  
  
  def __str__(self):
    return f"{self.user.first_name} {self.user.last_name} had {self.total} points"
  
  class Meta:
    ordering: ['week.season', 'week.week', 'total', 'tiebreaker.tiebreaker_points']
    
# ----------------------------------------------------------------------------------------------------------
    
class GameTime(models.Model):
    game_time_id = models.BigAutoField(primary_key=True)
    day = models.ForeignKey('Day', on_delete=models.CASCADE, null=True)
    game_time = models.TimeField()
    
    def __str__(self):
        return f"{self.day.day},  {self.game_time.strftime('%I:%M %p')}"
    
    class Meta:
        ordering: ['day.add_days', 'game_time']
        
# ----------------------------------------------------------------------------------------------------------
        
class Day(models.Model):
    day_id = models.BigAutoField(primary_key=True)
    day = models.CharField(max_length=20)
    add_days = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(6)])
    
    def __str__(self):
        return f"{self.day}"
    
    class Meta:
        ordering: ['add_days']