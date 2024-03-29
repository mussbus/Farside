# Generated by Django 4.2.4 on 2023-12-10 00:53

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0014_alter_game_options_remove_game_start_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='game_status',
            field=models.CharField(blank=True, choices=[('', '---'), ('1', '1Q'), ('2', '2Q'), ('1', '3Q'), ('4', '4Q'), ('F', 'F')], default='N', max_length=1),
        ),
        migrations.AlterField(
            model_name='pick',
            name='submit_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 9, 18, 53, 32, 932892)),
        ),
        migrations.AlterField(
            model_name='season',
            name='year_end',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 9, 18, 53, 32, 931893)),
        ),
        migrations.AlterField(
            model_name='season',
            name='year_start',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 9, 18, 53, 32, 931893)),
        ),
        migrations.AlterField(
            model_name='team',
            name='abbreviation',
            field=models.CharField(max_length=3, validators=[django.core.validators.MaxLengthValidator(2), django.core.validators.MinLengthValidator(3)]),
        ),
        migrations.AlterField(
            model_name='tiebreaker',
            name='submit_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 9, 18, 53, 32, 932892)),
        ),
    ]
