# Generated by Django 4.2 on 2023-04-27 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournoisApp', '0007_alter_match_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='Date',
            field=models.DateTimeField(null=True),
        ),
    ]
