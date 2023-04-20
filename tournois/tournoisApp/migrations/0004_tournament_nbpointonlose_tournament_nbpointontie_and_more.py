# Generated by Django 4.2 on 2023-04-20 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournoisApp', '0003_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='NBPointOnLose',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='tournament',
            name='NBPointOnTie',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='tournament',
            name='NBPointOnWin',
            field=models.IntegerField(default=3),
        ),
    ]
