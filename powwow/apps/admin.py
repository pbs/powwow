from django.contrib import admin
from powwow.apps.models import AppSettings

class AppSettingsAdmin(admin.ModelAdmin):
    list_display = ('name', 'content')

admin.site.register(AppSettings, AppSettingsAdmin)
