# Generated by Django 5.1 on 2024-08-14 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0002_player_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
