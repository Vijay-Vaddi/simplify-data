# Generated by Django 5.1 on 2024-08-16 18:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fixtures', '0002_rename_goals_goal_rename_period_periods_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fixture',
            old_name='period',
            new_name='periods',
        ),
    ]
