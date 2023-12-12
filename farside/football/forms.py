from django import forms
from .models import *
from django.forms import ModelForm
from django.forms import BaseFormSet
from football.models import Game

# --------------------------------------------------------------------------------------------------------------

# class GameForm(forms.Form):
#     # away_team = forms.ModelChoiceField(queryset=Team.objects.all().order_by('location', 'name'), empty_label=None)
#     # home_team = forms.ModelChoiceField(queryset=Team.objects.all().order_by('location', 'name'), empty_label=None)
#     game_time = forms.ChoiceField(choices=Game.STATUS)
    
#     class Meta:
#         widgets = {
#             # 'away_team':forms.Select(attrs={'class': 'input__select'}),
#             # 'home_team':forms.Select(attrs={'class': 'input__select'}),
#             'game_status':forms.Select(attrs={'class': 'input__select'})
#             }
        
class GameForm(forms.Form):
    game_time = forms.ChoiceField(choices=Game.STATUS)
    
    class Meta:
        widgets = {
            'game_status':forms.Select(attrs={'class': 'input__select'})
            }

# --------------------------------------------------------------------------------------------------------------

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
 
# --------------------------------------------------------------------------------------------------------------
    
class TiebreakerForm(ModelForm):    
    class Meta:
        model = Tiebreaker
        fields = ['tiebreaker_points']
        # fields = '__all__'
        widgets = {'tiebreaker_points':forms.NumberInput(attrs={'class': 'input__number'})}
        
    def clean(self):
        form_data = self.cleaned_data
    
        if form_data['tiebreaker_points'] < 0:
            self._errors['tiebreaker_points'] = 'Tiebreaker must be a non negative integer'
      
        return form_data
    
# --------------------------------------------------------------------------------------------------------------
    
class PickForm(forms.Form):
    home_team_points = forms.ChoiceField(label_suffix='', widget=forms.Select(attrs={'class': 'input__select'}), required=True)
    away_team_points = forms.ChoiceField(label_suffix='', widget=forms.Select(attrs={'class': 'input__select'}), required=True)
    game_id = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'input__number'}))
    away_team_id = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'input__number'}))
    home_team_id = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'input__number'}))
    pick_id = forms.IntegerField(initial=-1, widget=forms.NumberInput(attrs={'class': 'input__number'}))
    
    def clean(self):
        form_data = self.cleaned_data
    
        if int(form_data['home_team_points']) < 0 and int(form_data['away_team_points']) < 0:
            game = Game.objects.get(game_id=form_data['game_id'])
            self._errors['home_team_points'] = f'({game.away_team.abbreviation} at {game.home_team.abbreviation}) - No team selected.'
        elif int(form_data['home_team_points']) > 0 and int(form_data['away_team_points']) > 0:
            self._errors['home_team_points'] = 'Both teams selected.'
      
        return form_data
    
# class PickFormSet(forms.BaseFormSet):
#     def clean(self):
#         formset_data = self.cleaned_data
        
#         pick_list = list()
        
#         for form in formset_data:
#             if form['away_team_points'] != '':                
#                 if form['away_team_points'] in pick_list and form['away_team_points'] != '':
#                 pick_list.append(form['away_team_points'])
#             else if form['home_team_points'] != '':
#             else:
#                 self.errors += 
            
        
#         return formset_data