# Generated by Django 4.2 on 2023-05-03 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournoisApp', '0013_alter_match_score1_alter_match_score2'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='Round',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]