import os
import datetime
from django import template
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Count, Min, Sum
from django.http import JsonResponse
from django.contrib.auth.models import Group
from django.utils import timezone
from analytics.models import *


register = template.Library()


# Consolidated Reports tags
@register.simple_tag(name='yearly_consolidate_report')
def yearly_consolidate_report(year, store_id, sheet_head_id):
    
    total = WeeklyConsolidateDetail.objects.filter(consolidate__year=year,
                                                    consolidate__store__id=store_id,
                                                    head__id = sheet_head_id
                                                    ).aggregate(total=Sum('amount'))['total']   
    return total
        

@register.simple_tag(name='yearly_consolidate_total_by_sheet_head')
def yearly_consolidate_total_by_sheet_head(year, sheet_head_id):
    
    total = WeeklyConsolidateDetail.objects.filter(consolidate__year=year,
                                                    head__id = sheet_head_id
                                                    ).aggregate(total=Sum('amount'))['total']   
    return total


@register.simple_tag(name='yearly_consolidate_report_by_store')
def yearly_consolidate_report_by_store(year, store_id):
    
    total = WeeklyConsolidateDetail.objects.filter(consolidate__year=year,
                                                    consolidate__store__id=store_id,
                                                    ).aggregate(total=Sum('amount'))['total']   
    return total









        
@register.simple_tag(name='periodically_consolidate_report')
def periodically_store_level_report(year, sheet_head_id, start_date, end_date):
    
    total = WeeklyConsolidateDetail.objects.filter(consolidate__year=year,
                                                    head__id = sheet_head_id,
                                                    consolidate__week__start_date__gte=start_date,
                                                    consolidate__week__start_date__lte=end_date,
                                                    ).aggregate(total=Sum('amount'))['total']  
    return total






@register.simple_tag(name='weekly_consolidate_report')
def weekly_consolidate_report(year, sheet_head_id, week_id):
    total = WeeklyConsolidateDetail.objects.filter(consolidate__year=year,
                                                    head__id = sheet_head_id,
                                                    consolidate__week__id=week_id,
                                                    ).aggregate(total=Sum('amount'))['total']  
    return total


@register.simple_tag(name='weekly_consolidate_total')
def weekly_consolidate_total(year, sheet_head_id):
    total = WeeklyConsolidateDetail.objects.filter(consolidate__year=year,
                                                    head__id = sheet_head_id,
                                                    ).aggregate(total=Sum('amount'))['total']  
    return total





# Store level Report tags
@register.simple_tag(name='weekly_store_level_report')
def weekly_store_level_report(year, store_id, sheet_head_id, week_id):
    total = WeeklyConsolidateDetail.objects.filter(consolidate__year=year,
                                                    consolidate__store__id=store_id,
                                                    head__id = sheet_head_id,
                                                    consolidate__week__id=week_id,
                                                    ).aggregate(total=Sum('amount'))['total']  
    
    return total


@register.simple_tag(name='weekly_store_level_total_by_sheet_head')
def weekly_store_level_total_by_sheet_head(year, store_id, sheet_head_id):
    total = WeeklyConsolidateDetail.objects.filter(consolidate__year=year,
                                                    consolidate__store__id=store_id,
                                                    head__id = sheet_head_id,
                                                    ).aggregate(total=Sum('amount'))['total']  
    
    return total


@register.simple_tag(name='weekly_store_level_report_by_week')
def weekly_store_level_report_by_week(year, store_id, week_id):
    total = WeeklyConsolidateDetail.objects.filter(consolidate__year=year,
                                                    consolidate__store__id=store_id,
                                                    consolidate__week__id=week_id,
                                                    ).aggregate(total=Sum('amount'))['total']  
    
    return total






@register.simple_tag(name='periodically_store_level_report')
def periodically_store_level_report(year, store_id, sheet_head_id, start_date, end_date):
    
    total = WeeklyConsolidateDetail.objects.filter(consolidate__year=year,
                                                    consolidate__store__id=store_id,
                                                    head__id = sheet_head_id,
                                                    consolidate__week__start_date__gte=start_date,
                                                    consolidate__week__start_date__lte=end_date,
                                                    ).aggregate(total=Sum('amount'))['total']  
    return total


# Magaer level report tags
@register.simple_tag(name='weekly_by_manager_report')
def weekly_by_manager_report(year, manager_id, sheet_head_id, week_id):
    total = WeeklyConsolidateDetail.objects.filter(consolidate__year=year,
                                                    consolidate__store__manager__id=manager_id,
                                                    head__id = sheet_head_id,
                                                    consolidate__week__id=week_id,
                                                    ).aggregate(total=Sum('amount'))['total']  
    
    return total



@register.simple_tag(name='periodically_by_manager_report')
def periodically_by_manager_report(year, manager_id, sheet_head_id, start_date, end_date):
    
    total = WeeklyConsolidateDetail.objects.filter(consolidate__year=year,
                                                    consolidate__store__manager__id=manager_id,
                                                    head__id = sheet_head_id,
                                                    consolidate__week__start_date__gte=start_date,
                                                    consolidate__week__start_date__lte=end_date,
                                                    ).aggregate(total=Sum('amount'))['total']  
    return total


#zonal level report tags
@register.simple_tag(name='weekly_by_zone_report')
def weekly_by_zone_report(year, zone_id, sheet_head_id, week_id):
    total = WeeklyConsolidateDetail.objects.filter(consolidate__year=year,
                                                    consolidate__store__zone__id=zone_id,
                                                    head__id = sheet_head_id,
                                                    consolidate__week__id=week_id,
                                                    ).aggregate(total=Sum('amount'))['total']  
    
    return total


@register.simple_tag(name='periodically_by_zone_report')
def periodically_by_zone_report(year, zone_id, sheet_head_id, start_date, end_date):
    
    total = WeeklyConsolidateDetail.objects.filter(consolidate__year=year,
                                                    consolidate__store__zone__id=zone_id,
                                                    head__id = sheet_head_id,
                                                    consolidate__week__start_date__gte=start_date,
                                                    consolidate__week__start_date__lte=end_date,
                                                    ).aggregate(total=Sum('amount'))['total']  
    return total