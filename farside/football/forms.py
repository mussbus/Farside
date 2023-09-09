from django import forms
from .models import *
from django.forms import ModelForm

class TeamForm(ModelForm):
  class Meta:
    model = Team
    fields = '__all__'
    labels = {
      'abbreviation': 'Abbreviation',
      'location': 'Team Location',
      'name': 'Team Name'
    }
    error_messages = {
      'abbreviation': {
        'min_length': 'min length is 3',
        'max_length': 'max length is 3'
      }
    }
    
class PickForm(ModelForm):
  class Meta:
    model = Pick
    fields = ['value', 'week', 'team', 'game']
    widgets = {'value':forms.NumberInput(attrs={'class': 'input__value'}),
               'week':forms.NumberInput(attrs={'class': 'input__week'}),
               'team':forms.NumberInput(attrs={'class': 'input__team'}),
               'game':forms.NumberInput(attrs={'class': 'input__game'})}
    
class TiebreakerForm(ModelForm):
  class Meta:
    model = Tiebreaker
    fields = ['tiebreaker_points']
    widgets = {'tiebreaker_points':forms.NumberInput(attrs={'class': 'input__number'})}