from django.db import models
from django.contrib.auth.models import User


class Division(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название подразделения', unique=True)
    division_id = models.IntegerField(verbose_name='ID подразделения в системе Супервизор', unique=True)
    count_windows = models.PositiveIntegerField(verbose_name='Количество окон', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'
        indexes = [models.Index(fields=['name'])]
        ordering = ['name']


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь',null=True, blank=True)
    full_name = models.CharField(max_length=500, verbose_name='ФИО пользователя')
    divisions = models.ManyToManyField(Division, verbose_name='Подразделения')
    photo_base64 = models.TextField(verbose_name='Фото профиля в base64', null=True, blank=True)
    eo_database_username = models.CharField(max_length=100, null=True, blank=True,
                                            verbose_name='Имя пользователя в системе ЭО')
    eo_database_id = models.IntegerField(null=True, blank=True, unique=True,
                                         verbose_name='ID пользователя в системе ЭО')

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
        indexes = [models.Index(fields=['full_name'])]
        ordering = ['full_name']
