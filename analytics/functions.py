from datetime import datetime
import pandas as pd
from datetime import timedelta
from .models import *
from django.contrib import messages


def create_weeks(start_date, year):
    start = datetime.strptime(start_date, '%Y-%m-%d')
    counter = 1
    i = year
    
    while i == year:
        end = start.date() + timedelta(days=6)
        
        if str(end)[:4] == year:
            Week.objects.create(name=f"Week {counter}", year=year, start_date=start, end_date=end)
        
        start = datetime.strptime(str(end), '%Y-%m-%d') + timedelta(days=1)
        i = str(start.date())[:4]
        counter += 1
        
        
        
def create_periods(year):
    weeks = list(Week.objects.filter(year=year))
    list1 = weeks[::4]
    list2 = weeks[3::4]

    
    if weeks:
        for i in range(len(list2)):
            
            Period.objects.create(name=f"Period {i+1}", 
                                    year=year, 
                                    start_week=list1[i],
                                    end_week=list2[i]
                                    )
            
    else:
        print('Please add weeks for this year before.')
        
        
        
        
def read_file_and_add_date(year, week, file_url, sheet_name):
    stores = Store.objects.all()
    sheet_heads = SheetHead.objects.all().order_by('order')
    
    # Start reading file
    df = pd.read_excel(file_url, index_col=0, sheet_name=sheet_name)
    
    heads = df.keys().tolist()
    
    list = df.values.tolist()
    
    # Adding data to db
    for i in range(len(stores)):
        instance = WeeklyConsolidate.objects.create(year=year, week=Week.objects.get(id=week), store=stores[i])
        
        values = list[i]
    
        for j in range(len(sheet_heads)):
            if values[j] == 'nan':
                WeeklyConsolidateDetail.objects.create(consolidate=instance, head=sheet_heads[j], amount=0)
            else:
                WeeklyConsolidateDetail.objects.create(consolidate=instance, head=sheet_heads[j], amount=values[j])
        
    
    
def weeks_of_period(period_id):
    weeks = []
    
    period = Period.objects.get(id=period_id)
    week11 = period.start_week
    week4 = period.end_week
    
    
    return None