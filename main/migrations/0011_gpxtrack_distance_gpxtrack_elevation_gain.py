# Generated by Django 5.0.7 on 2024-09-14 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_remove_gpxtrack_distance_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='gpxtrack',
            name='distance',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='gpxtrack',
            name='elevation_gain',
            field=models.FloatField(default=0),
        ),
    ]
