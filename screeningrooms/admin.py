from django.contrib import admin
from .models import ScreeningRoom

@admin.register(ScreeningRoom)
class ScreeningRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'cinema', 'capacity')
    list_filter = ('cinema',)


