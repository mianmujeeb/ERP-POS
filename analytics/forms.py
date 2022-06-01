from django import forms
from .models import *


class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'


class SheetHeadForm(forms.ModelForm):

    class Meta:

        model = SheetHead
        fields ='__all__'



class ManagerForm(forms.ModelForm):

    class Meta:

        model = Manager
        fields = '__all__'




class StoreForm(forms.ModelForm):

    class Meta:

        model = Store
        fields = ('manager', 'zone', 'name', 'address', 'city', 'country',)


class WeekForm(forms.ModelForm):
    

    class Meta:

        model = Week
        fields = '__all__'
        widgets = {
            'start_date' : DateInput(),
            'end_date' : DateInput(),
        }
