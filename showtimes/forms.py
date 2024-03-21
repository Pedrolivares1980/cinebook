from django import forms
from .models import  ScreeningRoom, Movie, Showtime
from cinemas.models import Cinema
from django.utils import timezone

class ShowtimeForm(forms.ModelForm):
    class Meta:
        model = Showtime
        fields = '__all__'
        widgets = {
            'showtime': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%d-%m-%YT%H:%M'),
        }

    
    def __init__(self, *args, **kwargs):
        super(ShowtimeForm, self).__init__(*args, **kwargs)
        self.fields['showtime'].input_formats = ('%d-%m-%YT%H:%M',)

class ShowtimeFilterForm(forms.Form):
    cinema = forms.ModelChoiceField(queryset=Cinema.objects.all(), required=False, label="Cinema")
    screening_room = forms.ModelChoiceField(queryset=ScreeningRoom.objects.all(), required=False, label="Screening Room")
    movie = forms.ModelChoiceField(queryset=Movie.objects.all(), required=False, label="Movie")
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label="Start Date")
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label="End Date")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)