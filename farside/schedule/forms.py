from django import forms
from football.models import *
from django.forms import ModelForm

GAME_OPTIONS = [
  (12, '12'),
  (13, '13'),
  (14, '14'),
  (15, '15'),
  (16, '16')
]

WEEK_OPTIONS = [
  (-1, '---'),
  (1, '1'),
  (2, '2'),
  (3, '3'),
  (4, '4'),
  (5, '5'),
  (6, '6'),
  (7, '7'),
  (8, '8'),
  (9, '9'),
  (10, '10'),
  (11, '11'),
  (12, '12'),
  (13, '13'),
  (14, '14'),
  (15, '15'),
  (16, '16'),
  (17, '17'),
  (18, '18')
]

class GameForm(ModelForm):
    use_required_attribute = False
    class Meta:
        model = Game
        fields = ['game_time', 'away_team', 'home_team']
        widgets = {'game_time':forms.Select(attrs={'class': 'input__select input__select-large'}),
               'away_team':forms.Select(attrs={'class': 'input__select input__select-large'}),
               'home_team':forms.Select(attrs={'class': 'input__select input__select-large'})}
    
class ScoreForm(ModelForm):
    class Meta:
        model = Game
        fields = ['game_status', 'away_score', 'home_score']
        widgets = {'game_status':forms.Select(choices=Game.STATUS, attrs={'class': 'input__select'}),
                'away_score':forms.NumberInput(attrs={'class': 'input__number input__select-small'}),
                'home_score':forms.NumberInput(attrs={'class': 'input__number input__select-small'})}
    
class SearchWeekForm(forms.Form):
    season = forms.ModelChoiceField(queryset=Season.objects.all().order_by('year'),
                                widget=forms.Select(attrs={'class': 'input__select'}),
                                empty_label='---', required=True)  
  
    week = forms.ChoiceField(choices=WEEK_OPTIONS, required=True,
                           widget=forms.Select(attrs={'class': 'input__select'}))
    
class ScoreFormset(forms.BaseFormSet):
    def __init__(self, *args, **kwargs):
        super(ScoreFormset, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False
