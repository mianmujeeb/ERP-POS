from django.contrib import admin
from .models import *

# Register your models here.


    
    
    

@admin.register(SheetHead)
class SheetHeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    
    
@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
    
@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'zone', 'manager', 'address')
    list_filter = ('zone', 'manager')
    search_fields = ('name',)
    
    
@admin.register(Week)
class WeekAdmin(admin.ModelAdmin):

    list_display = ('name', 'start_date', 'end_date', 'year')
    list_filter = ('year',)
    


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):

    list_display = ('name', 'start_week', 'end_week', 'year')
    list_filter = ('year',)
    
    
@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):

    list_display = ('first_name', 'last_name', 'email', 'city', 'country')
    list_filter = ('city', 'country')
    search_fields = ('first_name', 'last_name')
    
    
    
class WeeklyConsolidateDetailInline(admin.TabularInline):
    model = WeeklyConsolidateDetail
@admin.register(WeeklyConsolidate)
class WeeklyConsolidateAdmin(admin.ModelAdmin):
    list_display = ('store', 'week', 'year')
    list_filter = ('store', 'week', 'year')
    inlines = [ WeeklyConsolidateDetailInline ]
    
    


class BudgetDetailInline(admin.StackedInline):
    model = BudgetDetail
    
@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('store', 'year', 'week', )
    list_filter = ('year',)
    inlines = [
        BudgetDetailInline,
    ]