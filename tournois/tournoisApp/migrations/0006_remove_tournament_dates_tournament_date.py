# Generated by Django 4.2 on 2023-04-20 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournoisApp', '0005_pool_teams'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tournament',
            name='Dates',
        ),
        migrations.AddField(
            model_name='tournament',
            name='Date',
            field=models.DateField(null=True),
        ),
    ]
