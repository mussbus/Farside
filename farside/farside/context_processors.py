# farside/context_processor.py
import datetime
from football.models import Week

def current_week_info(request):
  # current_time = datetime.datetime.now()
  current_time = datetime.datetime(2023, 9, 9, 0, 0, 0)
  # current_week_url_exist = request.session.get('current_week_url', False)
  boo_current_week = False
  if not boo_current_week:
    week = Week.objects.get(time_start__lt=current_time, time_end__gt=current_time)
    
    current_week_url = '/football/season/' + str(week.season.year) + '/week/' + str(week.week)
    current_week = week.week
    current_year = week.season.year
    
    request.session['current_week'] = current_week
    request.session['current_week_url'] = current_week_url
    request.session['current_year'] = current_year
  else:
    current_week = request.session['current_week']
    current_week_url = request.session['current_week_url']
    current_year = request.session['current_year']

  return {'current_week': current_week,
          'current_week_url': current_week_url,
          'current_year': current_year}