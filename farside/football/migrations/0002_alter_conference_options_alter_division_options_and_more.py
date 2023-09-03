# Generated by Django 4.2.4 on 2023-08-19 03:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='conference',
            options={'ordering': ['abbreviation']},
        ),
        migrations.AlterModelOptions(
            name='division',
            options={'ordering': ['conference', 'name']},
        ),
        migrations.AlterModelOptions(
            name='game',
            options={'ordering': ['week', 'start_time', 'game_id']},
        ),
        migrations.AlterModelOptions(
            name='season',
            options={'ordering': ['year']},
        ),
        migrations.AlterModelOptions(
            name='team',
            options={'ordering': ['location', 'name']},
        ),
        migrations.AlterModelOptions(
            name='week',
            options={'ordering': ['season', 'week']},
        ),
        migrations.RenameField(
            model_name='conference',
            old_name='Abbreviation',
            new_name='abbreviation',
        ),
        migrations.RenameField(
            model_name='conference',
            old_name='ConferenceID',
            new_name='conference_id',
        ),
        migrations.RenameField(
            model_name='conference',
            old_name='Name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='division',
            old_name='ConferenceID',
            new_name='conference',
        ),
        migrations.RenameField(
            model_name='division',
            old_name='DivisionID',
            new_name='division_id',
        ),
        migrations.RenameField(
            model_name='division',
            old_name='Name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='Away_Score',
            new_name='away_score',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='Away_TeamID',
            new_name='away_team',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='GameID',
            new_name='game_id',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='Game_Status',
            new_name='game_status',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='Home_Score',
            new_name='home_score',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='Home_TeamID',
            new_name='home_team',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='Start_Time',
            new_name='start_time',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='WeekID',
            new_name='week',
        ),
        migrations.RenameField(
            model_name='pick',
            old_name='GameID',
            new_name='game',
        ),
        migrations.RenameField(
            model_name='pick',
            old_name='PickID',
            new_name='pick_id',
        ),
        migrations.RenameField(
            model_name='pick',
            old_name='TeamID',
            new_name='team',
        ),
        migrations.RenameField(
            model_name='pick',
            old_name='UserID',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='pick',
            old_name='Point',
            new_name='value',
        ),
        migrations.RenameField(
            model_name='pick',
            old_name='WeekID',
            new_name='week',
        ),
        migrations.RenameField(
            model_name='season',
            old_name='SeasonID',
            new_name='season_id',
        ),
        migrations.RenameField(
            model_name='season',
            old_name='Year',
            new_name='year',
        ),
        migrations.RenameField(
            model_name='team',
            old_name='Abbreviation',
            new_name='abbreviation',
        ),
        migrations.RenameField(
            model_name='team',
            old_name='DivisionID',
            new_name='division',
        ),
        migrations.RenameField(
            model_name='team',
            old_name='Location',
            new_name='location',
        ),
        migrations.RenameField(
            model_name='team',
            old_name='Name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='team',
            old_name='TeamID',
            new_name='team_id',
        ),
        migrations.RenameField(
            model_name='tiebreaker',
            old_name='GameID',
            new_name='game',
        ),
        migrations.RenameField(
            model_name='tiebreaker',
            old_name='TiebreakerID',
            new_name='tiebreaker_id',
        ),
        migrations.RenameField(
            model_name='tiebreaker',
            old_name='Tiebreaker_Points',
            new_name='tiebreaker_points',
        ),
        migrations.RenameField(
            model_name='tiebreaker',
            old_name='UserID',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='tiebreaker',
            old_name='WeekID',
            new_name='week',
        ),
        migrations.RenameField(
            model_name='week',
            old_name='SeasonID',
            new_name='season',
        ),
        migrations.RenameField(
            model_name='week',
            old_name='TimeEnd',
            new_name='time_end',
        ),
        migrations.RenameField(
            model_name='week',
            old_name='TimeStart',
            new_name='time_start',
        ),
        migrations.RenameField(
            model_name='week',
            old_name='Week',
            new_name='week',
        ),
        migrations.RenameField(
            model_name='week',
            old_name='WeekID',
            new_name='week_id',
        ),
        migrations.RemoveField(
            model_name='pick',
            name='Submit_Date',
        ),
        migrations.RemoveField(
            model_name='tiebreaker',
            name='Submit_Date',
        ),
        migrations.AddField(
            model_name='pick',
            name='submit_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 18, 22, 44, 31, 476350)),
        ),
        migrations.AddField(
            model_name='tiebreaker',
            name='submit_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 18, 22, 44, 31, 476350)),
        ),
    ]