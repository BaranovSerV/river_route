# Generated by Django 5.0.7 on 2024-09-13 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_topic_author_alter_topic_content_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='GPXTrack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('gpx_file', models.FileField(upload_to='gpx_tracks/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
