# Generated by Django 4.2 on 2023-05-03 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournoisApp', '0010_match_lattitude_match_longitude'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='Date',
            field=models.DateTimeField(),
        ),
    ]
