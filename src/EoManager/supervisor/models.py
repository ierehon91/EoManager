from django.db import models
from django.contrib.auth.models import User


class Division(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название подразделения')
    division_id = models.IntegerField(verbose_name='ID подразделения в системе Супервизор')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    divisions = models.ManyToManyField(Division)
