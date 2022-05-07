from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Capital(models.Model):
    capital_text = models.CharField(max_length=255)
    pub_date = models.DateTimeField('date published')


class Option(models.Model):
    capital = models.ForeignKey(Capital, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    correct = models.BooleanField(default=False)


class Mark(models.Model):
    capital = models.ForeignKey(
        Capital,
        verbose_name='Страна & столица',
        on_delete=models.CASCADE)
    author = models.ForeignKey(
        User,
        verbose_name='Пользователь', on_delete=models.CASCADE)
    mark = models.IntegerField(
        verbose_name='Оценка')
    pub_date = models.DateTimeField(
        'Дата оценки',
        default=timezone.now)
