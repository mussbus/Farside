# Generated by Django 4.1.3 on 2023-11-24 04:13

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0013_alter_pick_submit_date_alter_season_year_end_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='game',
            options={},
        ),
        migrations.RemoveField(
            model_name='game',
            name='start_time',
        ),
        migrations.AddField(
            model_name='game',
            name='game_time',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='football.gametime'),
        ),
        migrations.AlterField(
            model_name='pick',
            name='submit_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 23, 22, 13, 15, 494048)),
        ),
        migrations.AlterField(
            model_name='season',
            name='year_end',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 23, 22, 13, 15, 493051)),
        ),
        migrations.AlterField(
            model_name='season',
            name='year_start',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 23, 22, 13, 15, 493051)),
        ),
        migrations.AlterField(
            model_name='tiebreaker',
            name='submit_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 23, 22, 13, 15, 494048)),
        ),
    ]
