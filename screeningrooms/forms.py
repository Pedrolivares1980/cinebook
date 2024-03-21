from django import forms
from .models import ScreeningRoom

class ScreeningRoomForm(forms.ModelForm):
    class Meta:
        model = ScreeningRoom
        fields = ['cinema', 'name', 'capacity', 'seats_per_row']
        labels = {
            'cinema': 'Cinema',
            'name': 'Name',
            'capacity': 'Capacity',
        }
        help_texts = {
            'name': 'Enter the name of the screening room.',
            'capacity': 'Select the capacity of the screening room.',
        }

    def __init__(self, *args, **kwargs):
        super(ScreeningRoomForm, self).__init__(*args, **kwargs)
        self.fields['seats_per_row'].initial = 10
        self.fields['seats_per_row'].widget = forms.HiddenInput()
        self.fields['capacity'].widget = forms.Select(choices=ScreeningRoom.CAPACITY_CHOICES)

