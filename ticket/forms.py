from pyexpat import model
from turtle import textinput
from django import forms
from django.forms import ModelForm
#from .models import Bus
#from .models import Air
#from .models import Train
from service.models import Bus,Air,Train
class BusForm(forms.ModelForm):
    class Meta:
        model=Bus
        fields='__all__'
class AirForm(forms.ModelForm):
    class Meta:
        model=Air
        fields='__all__'
class TForm(forms.ModelForm):
    class Meta:
        model=Train
        fields='__all__'