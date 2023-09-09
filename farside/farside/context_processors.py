# farside/context_processor.py
import datetime
from football.models import Week

def current_week(request):
  # current_time = datetime.datetime.now()
  current_time = datetime.datetime(2023, 9, 9, 0, 0, 0)
  # current_week_exist = request.session.get('current_week', 'null')
  current_week_exist = 'null'
  if current_week_exist == 'null':
    week = Week.objects.get(time_start__lt=current_time, time_end__gt=current_time)
    current_week = '/football/season/' + str(week.season.year) + '/week/' + str(week.week)
    request.session['current_week'] = current_week
  else:
    current_week = request.session['current_week']

  return {'current_week': current_week}