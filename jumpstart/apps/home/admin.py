from django.contrib import admin
from jumpstart.apps.home.models import Idea

@admin.register(Idea)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'poster')
