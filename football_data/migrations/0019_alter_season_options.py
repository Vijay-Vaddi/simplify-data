# Generated by Django 5.1 on 2024-08-17 14:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('football_data', '0018_alter_venue_venue_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='season',
            options={'ordering': ['year']},
        ),
    ]
