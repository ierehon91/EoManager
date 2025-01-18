from django.contrib import admin
from . import models


@admin.register(models.Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ('name', 'division_id', 'count_windows')


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name','eo_database_id', 'eo_database_username')
