from django.contrib import admin

from .models import Rating, Spot, Visitor


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "age")


@admin.register(Spot)
class SpotAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "location", "category")


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("id", "visitor", "spot", "score", "comment")
