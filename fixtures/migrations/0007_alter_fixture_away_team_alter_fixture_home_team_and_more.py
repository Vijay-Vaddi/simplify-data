# Generated by Django 5.1 on 2024-08-18 12:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fixtures', '0006_fixture_score'),
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fixture',
            name='away_team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fixtures_away', to='teams.team'),
        ),
        migrations.AlterField(
            model_name='fixture',
            name='home_team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fixtures_home', to='teams.team'),
        ),
        migrations.AlterField(
            model_name='fixture',
            name='venue',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fixtures', to='teams.venue'),
        ),
    ]
