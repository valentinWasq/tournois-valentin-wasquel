# Generated by Django 4.2 on 2023-05-04 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournoisApp', '0018_merge_0016_alter_match_pool_0017_merge_20230504_2011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='Location',
            field=models.CharField(max_length=50, null=True),
        ),
    ]