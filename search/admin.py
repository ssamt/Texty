from django.contrib import admin
from django.contrib.auth.models import User, Group
from . import models

admin.site.unregister(User)
admin.site.unregister(Group)

@admin.register(models.Page)
class GaonnuriPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'website', 'author', 'time', 'default_importance', 'manual_importance')
    list_filter = ['website', 'author']
