from django import forms
from .models import Room, Reservation


class AddRoomForm(forms.ModelForm):

    class Meta:
        model = Room
        fields = (
            'name',
            'capacity',
            'projector')


class AddReservationForm(forms.ModelForm):

    date = forms.DateField(widget=forms.SelectDateWidget())
    class Meta:
        model = Reservation
        fields = (
            '__all__')
