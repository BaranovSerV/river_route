# models.py
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg')

    def __str__(self):
        return self.user.username
    
    
class Topic(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название темы')
    content = models.TextField(verbose_name='Содержание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    views = models.PositiveIntegerField(default=0, verbose_name='Количество просмотров')  # Счетчик просмотров



class Report(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('in_progress', 'In Progress'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    

class GPXTrack(models.Model):
    name = models.CharField(max_length=200)
    file = models.FileField(upload_to='gpx_tracks/')
    description = models.TextField(blank=True, null=True)
    distance = models.FloatField(default=0)  # Длина маршрута в километрах
    elevation_gain = models.FloatField(default=0)  # Набор высоты в метрах

    def __str__(self):
        return self.name