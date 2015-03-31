from django.contrib import admin
from jumpstart.apps.home.models import Idea, Category, Rating

class RatingInline(admin.TabularInline):
    model = Rating
    extra = 1

@admin.register(Idea)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'net_rating')
    inlines = [RatingInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass