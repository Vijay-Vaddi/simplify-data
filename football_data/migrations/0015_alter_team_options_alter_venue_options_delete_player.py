# Generated by Django 5.1 on 2024-08-14 09:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('football_data', '0014_alter_team_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='team',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='venue',
            options={'ordering': ['name']},
        ),
        migrations.DeleteModel(
            name='Player',
        ),
    ]
