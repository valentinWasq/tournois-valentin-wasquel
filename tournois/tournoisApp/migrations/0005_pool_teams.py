# Generated by Django 4.2 on 2023-04-20 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournoisApp', '0004_tournament_nbpointonlose_tournament_nbpointontie_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pool',
            name='Teams',
            field=models.ManyToManyField(to='tournoisApp.team'),
        ),
    ]