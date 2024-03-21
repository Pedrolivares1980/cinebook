from django.contrib import admin
from .models import Showtime
from .forms import ShowtimeForm

class ShowtimeAdmin(admin.ModelAdmin):
    form = ShowtimeForm

admin.site.register(Showtime, ShowtimeAdmin)
