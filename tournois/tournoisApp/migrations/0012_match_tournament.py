# Generated by Django 4.2 on 2023-05-03 04:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournoisApp', '0011_match_ispool'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='Tournament',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='tournoisApp.tournament'),
        ),
    ]