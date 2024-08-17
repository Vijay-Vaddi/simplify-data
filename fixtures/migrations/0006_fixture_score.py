# Generated by Django 5.1 on 2024-08-17 17:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fixtures', '0005_alter_status_options_league_season'),
    ]

    operations = [
        migrations.AddField(
            model_name='fixture',
            name='score',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fixtures_score', to='fixtures.score'),
        ),
    ]
