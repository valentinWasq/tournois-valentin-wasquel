# Generated by Django 4.2 on 2023-04-20 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournoisApp', '0006_remove_tournament_dates_tournament_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='Date',
            field=models.DateField(null=True),
        ),
    ]