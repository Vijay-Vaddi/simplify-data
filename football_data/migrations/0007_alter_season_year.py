# Generated by Django 5.1 on 2024-08-11 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football_data', '0006_alter_season_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='season',
            name='year',
            field=models.IntegerField(editable=False, unique=True),
        ),
    ]
