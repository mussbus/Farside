from django.db import models
from django.core.validators import *
from django.contrib.auth.models import User 
import datetime

# Create your models here.

class Time(models.Model):
  time_id = models.BigAutoField(primary_key=True)
  day = models.ForeignKey('Day', on_delete=models.CASCADE, null=True)
  time = models.TimeField()
  
  def __str__(self):
    return f"{self.day.day} - {self.time}"
  
  class Meta:
    ordering = ['day__day', 'time']
    
class Day(models.Model):
  day_id = models.BigAutoField(primary_key=True)
  day = models.CharField(validators=[MinLengthValidator(5), MaxLengthValidator(10)], max_length=10)
  add_day = models.IntegerField()
  
  def __str__(self):
    return f"{self.day}"
  
  class Meta:
    ordering = ['add_day']
