import django_filters as filters
from django_filters import CharFilter
from django.forms.widgets import TextInput
from .models import *



class WeekFilter(filters.FilterSet):
    year = CharFilter(field_name='year', lookup_expr='iexact', label='Search:', widget=TextInput(attrs={'placeholder': 'Filter by year...'}))
    
    class Meta:
        model = Week
        fields = ('year',)
        
        
        
class ManagerFilter(filters.FilterSet):
    year = CharFilter(field_name='year', lookup_expr='iexact', label='Search:', widget=TextInput(attrs={'placeholder': 'Filter by year...'}))
    
    class Meta:
        model = Week
        fields = ('year',)