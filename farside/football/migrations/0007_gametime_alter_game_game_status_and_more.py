# Generated by Django 4.1.3 on 2023-11-24 03:25

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0006_season_year_end_season_year_start_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameTime',
            fields=[
                ('game_time_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('add_days', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(6)])),
                ('day_of_week', models.CharField(max_length=20)),
                ('game_time', models.TimeField()),
            ],
        ),
        migrations.AlterField(
            model_name='game',
            name='game_status',
            field=models.CharField(blank=True, choices=[('', 'Not Started'), ('1', '1Q'), ('2', '2Q'), ('1', '3Q'), ('4', '4Q'), ('F', 'Finished')], default='N', max_length=1),
        ),
        migrations.AlterField(
            model_name='pick',
            name='submit_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 23, 21, 25, 9, 30463)),
        ),
        migrations.AlterField(
            model_name='season',
            name='year_end',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 23, 21, 25, 9, 30463)),
        ),
        migrations.AlterField(
            model_name='season',
            name='year_start',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 23, 21, 25, 9, 30463)),
        ),
        migrations.AlterField(
            model_name='tiebreaker',
            name='submit_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 23, 21, 25, 9, 30463)),
        ),
        migrations.AlterField(
            model_name='tiebreaker',
            name='tiebreaker_points',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1000)]),
        ),
    ]
