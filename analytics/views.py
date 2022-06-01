from gc import get_objects
import pandas as pd
from .forms import *
from .models import *
from .filters import *
from .functions import *
from pprint import pprint
from .decorators import *
from datetime import datetime
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Avg, Count, Min, Sum
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

# Create your views here.


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Welcome on the board')
            
            if 'next' in request.POST:
                return redirect(request.POST['next'])
            else:
                return redirect('analytics:dashboard')
        else:
            messages.warning(request, 'Invalid credentials')
            
    return render(request, 'login.html')


def logout(request):
    auth_logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('analytics:login')



@login_required
def dashboard(request):
    total_zones = Zone.objects.all().count()
    total_stores = Store.objects.all().count()
    total_managers = Manager.objects.all().count()
    
    context = {
        'total_zones' : total_zones,
        'total_stores' : total_stores, 
        'total_managers' : total_managers
    }
    return render(request, 'dashboard.html', context)
    


@login_required
def managers(request):
    managers = Manager.objects.all().order_by('-id')
    
    context = {
        'managers' : managers,
    }
    return render(request, 'managers.html', context)


@login_required
def addManager(request):
    form = ManagerForm()
    
    if request.method == 'POST':
        form = ManagerForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Manager addedd successfully')
            return redirect('analytics:managers')
    
    context = {
        'form' : form,
    }
    return render(request, 'add-manager.html', context)


@login_required
def updateManager(request, pk):
    manager = get_object_or_404(Manager, id=pk)
    form = ManagerForm(instance=manager)
    
    if request.method == 'POST':
        form = ManagerForm(request.POST,instance=manager)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Manager updated successfully')
            return redirect('analytics:managers')
    
    context = {
        'manager' : manager,
        'form' : form,
    }
    return render(request, 'update-manager.html', context)

@login_required
def deleteManager(request, pk):
    manager = get_object_or_404(Manager, id=pk)
    manager.delete()
    messages.info(request, 'Manager deleted successfully')
    return redirect('analytics:managers')


@login_required
def zones(request):
    zones = Zone.objects.all().order_by('name')
    
    if request.method == 'POST':
        if 'addZone' in request.POST:
            name = request.POST.get('name')
            Zone.objects.create(name=name, added_by=request.user)
            messages.success(request, 'Zone addedd successfully')
            return redirect('analytics:zones')
        
        if 'updateZone' in request.POST:
            zone = get_object_or_404(Zone, id=request.POST.get('zone_id__update'))
            zone.name = request.POST.get('name__update')
            zone.save()
            messages.success(request, 'Zone updated successfully')
            return redirect('analytics:zones')
        
        if 'deleteZone' in request.POST:
            zone = get_object_or_404(Zone, id=request.POST.get('zone_id__delete'))
            zone.delete()
            messages.info(request, 'Zone deleted successfully')
            return redirect('analytics:zones')
            
    
    context = {
        'zones' : zones
    }
    return render(request, 'zones.html', context)



@login_required
def stores(request):
    stores = Store.objects.all()
    
    context = {
        'stores' : stores,
    }
    return render(request, 'stores.html', context)


@login_required
def addStore(request):
    form = StoreForm()
    
    if request.method == 'POST':
        form = StoreForm(request.POST)
        
        if form.is_valid():
            store = form.save(commit=False)
            store.added_by = request.user
            store.save()
            messages.success(request, 'Store addedd successfully')
            return redirect('analytics:stores')
    
    context = {
        'form' : form,
    }
    return render(request, 'add-store.html', context)


@login_required
def updateStore(request, pk):
    store = get_object_or_404(Store, id=pk)
    form = StoreForm(instance=store)
    
    if request.method == 'POST':
        form = StoreForm(request.POST, instance=store)
        
        if form.is_valid():
            store = form.save()
            messages.success(request, 'Store updated successfully')
            return redirect('analytics:stores')
    
    context = {
        'store' : store,
        'form' : form,
    }
    return render(request, 'update-store.html', context)


@login_required
def deleteStore(request, pk):
    store = get_object_or_404(Store, id=pk)
    store.delete()
    messages.info(request, 'Store deleted successfully')
    return redirect('analytics:stores')



@login_required
def sheetHeads(request):
    heads = SheetHead.objects.all().order_by('-order')
    
    if request.method == 'POST':
        if 'addSheetHead' in request.POST:
            name = request.POST.get('name')
            order = request.POST.get('order')
            SheetHead.objects.create(name=name, order=order)
            messages.success(request, 'sheet Head addedd successfully')
            return redirect('analytics:sheet-heads')
        
        if 'updateSheetHead' in request.POST:
            sheet_head = get_object_or_404(SheetHead, id=request.POST.get('sheet_head_id__update'))
            sheet_head.name = request.POST.get('sheet_head_name__update')
            sheet_head.order = request.POST.get('sheet_head_order__update')
            sheet_head.save()
            messages.success(request, 'Sheet Head updated successfully')
            return redirect('analytics:sheet-heads')
        
        if 'deleteSheetHead' in request.POST:
            sheet_head = get_object_or_404(SheetHead, id=request.POST.get('sheet_head_id__delete'))
            sheet_head.delete()
            messages.info(request, 'Sheet Head deleted successfully')
            return redirect('analytics:sheet-heads')
            
    
    context = {
        'heads' : heads
    }
    return render(request, 'sheet-heads.html', context)



@login_required
def filterWeeksAjax(request):
    year = request.GET.get('year')
    weeks = Week.objects.filter(year=year)
    
    context = {
        'weeks' : weeks,
    }
    return render(request, 'snippets/weeks-filtered.html', context)

@login_required
def weeksSetting(request):
    weeks = Week.objects.all().order_by('year')
    periods = Period.objects.all().order_by('year')
    filter_week = WeekFilter(request.GET, queryset=weeks)
    weeks_list = filter_week.qs
    
    if request.method == 'POST':
        if "addWeeks" in request.POST:
            year = request.POST.get('year')
            start_date = request.POST.get('start_date')
            if Week.objects.filter(year=year).exists():
                messages.warning(request, f'Weeks for {year} are already added')
                return redirect('analytics:weeks')
            else:
                create_weeks(start_date, year)
                create_periods(year)
                messages.success(request, f'Weeks are successfully added for {year}')
                return redirect('analytics:weeks')
            
    context = {
        'weeks' : weeks_list,
        'filter' : filter_week,
        'periods' : periods,
    }
    return render(request, 'weeks-settings.html', context)


@login_required
def updateWeek(request, pk):
    week = get_object_or_404(Week, id=pk)
    form = WeekForm(instance=week)
    
    if request.method == 'POST':
        form = WeekForm(request.POST, instance=week)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Week updated successfully')
            return redirect('analytics:weeks')
    
    context = {
        'week' : week,
        'form' : form,
    }
    return render(request, 'update-week-setting.html', context)



@login_required
def consolidates(request):
    consolidates = WeeklyConsolidate.objects.all().values_list('store__name', flat=True).distinct()
    
    
    context = {
        'list' : consolidates,
    }
    return render(request, 'consolidates.html', context)


@login_required
def consolidateDetail(request, store_name):
    
    consolidates = WeeklyConsolidate.objects.filter(store__name=store_name)
    
    context = {
        'store' : store_name,
        'list' : consolidates,
    }
    return render(request, 'consolidates-details.html', context)



@login_required
def consolidateYears(request):
    years = WeeklyConsolidate.objects.all().values_list('year', flat=True).distinct()
    
    context = {
        'years': years,
    }
    return render(request, 'weekly-consolidate-years.html', context)


@login_required
def consolidateByYears(request, year):
    consolidates = WeeklyConsolidate.objects.filter(year=year)
    
    context = {
        'list': consolidates,
        'year' : year,
    }
    return render(request, 'weekly-consolidate-by-years.html', context)


@login_required
def consolidateDetailsDetails(request):
    instance = get_object_or_404(WeeklyConsolidate, id=request.GET.get('id'))
    details = instance.consolidate_detail.all()
    
    
    context = {
        'instance' : instance,
        'details' : details,
    }
    return render(request, 'snippets/consolidate-details-details.html', context)



@login_required
def addConsolidate(request):
    year = datetime.today().year
    years = [datetime.today().year - index for index in range(5)]
    weeks = Week.objects.filter(year=year)
    
    if request.method == 'POST':
        year_input = request.POST.get('year')
        week = request.POST.get('week')
        sheet_name = request.POST.get('sheet_name')
        file = request.FILES.get('file')
        
        read_file_and_add_date(year_input, week, file, sheet_name)
        messages.success(request, f'Conslidate of {sheet_name} is addedd successfully')
        
    context = {
        'years' : years, 
        'weeks' : weeks,
    }
    return render(request, 'add-consolidate.html', context)




# REPORTES


# Consolidated
@login_required
def yearlyConsolidateReport(request):
    stores = Store.objects.all()
    sheet_heads = SheetHead.objects.all()
    
    if request.method == 'GET':
        year = request.GET.get('year')
        
    
    context = {
        'year' : year,
        'stores' : stores,
        'sheet_heads' : sheet_heads
    }
    return render(request, 'reports/yearly-consolidate-report.html', context)

@login_required
def periodicallyConsolidateReport(request):
    sheet_heads = SheetHead.objects.all()
    periods = None
    
    if request.method == 'GET':
        year = request.GET.get('year')
        if year:
            periods = Period.objects.filter(year=year)
        
    
    context = {
        'year' : year,
        'sheet_heads' : sheet_heads,
        'periods' : periods,
    }
    return render(request, 'reports/periodically-consolidate-report.html', context)

@login_required
def weeklyConsolidateReport(request):
    sheet_heads = SheetHead.objects.all()
    weeks = None
    
    if request.method == 'GET':
        year = request.GET.get('year')
        if year:
            weeks = Week.objects.filter(year=year)
        
    
    context = {
        'year' : year,
        'stores' : stores,
        'sheet_heads' : sheet_heads,
        'weeks' : weeks,
    }
    return render(request, 'reports/weekly-consolidate-report.html', context)


# By manager
@login_required
def weeklyConsolidateReportByManager(request):
    managers = Manager.objects.all()
    sheet_heads = SheetHead.objects.all()
    manager = None
    weeks = None
    
    if request.method == 'GET':
        year = request.GET.get('year')
        manager_id = request.GET.get('manager_id')
        if manager_id:
            manager = get_object_or_404(Manager, id=manager_id)
        if year:
            weeks = Week.objects.filter(year=year)
        
    
    context = {
        'year' : year,
        'managers' : managers,
        'sheet_heads' : sheet_heads,
        'manager_id' : manager_id,
        'manager' : manager,
        'weeks' : weeks,
    }
    return render(request, 'reports/weekly-by-manager-report.html', context)


@login_required
def periodicallyConsolidateReportByManager(request):
    managers = Manager.objects.all()
    sheet_heads = SheetHead.objects.all()
    manager = None
    periods = None
    
    if request.method == 'GET':
        year = request.GET.get('year')
        manager_id = request.GET.get('manager_id')
        if manager_id:
            manager = get_object_or_404(Manager, id=int(manager_id))
        if year:
            periods = Period.objects.filter(year=year)
    
    context = {
        'year' : year,
        'managers' : managers,
        'sheet_heads' : sheet_heads,
        'manager_id' : manager_id,
        'manager' : manager,
        'periods' : periods,
    }
    return render(request, 'reports/periodically-by-manager-report.html', context)




# Store Level
@login_required
def weeklyConsolidateReportByStore(request):
    stores = Store.objects.all()
    sheet_heads = SheetHead.objects.all()
    store = None
    weeks = None
    
    if request.method == 'GET':
        year = request.GET.get('year')
        store_id = request.GET.get('store_id')
        if store_id:
            store = get_object_or_404(Store, id=store_id)
        if year:
            weeks = Week.objects.filter(year=year)
        
    
    context = {
        'year' : year,
        'stores' : stores,
        'sheet_heads' : sheet_heads,
        'stor_id' : store_id,
        'store' : store,
        'weeks' : weeks,
    }
    return render(request, 'reports/weekly-store-level-report.html', context)


@login_required
def periodicallyConsolidateReportByStore(request):
    stores = Store.objects.all()
    sheet_heads = SheetHead.objects.all()
    store = None
    periods = None
    
    if request.method == 'GET':
        year = request.GET.get('year')
        store_id = request.GET.get('store_id')
        if store_id:
            store = get_object_or_404(Store, id=store_id)
        if year:
            periods = Period.objects.filter(year=year)
    
    context = {
        'year' : year,
        'stores' : stores,
        'sheet_heads' : sheet_heads,
        'stor_id' : store_id,
        'store' : store,
        'periods' : periods,
    }
    return render(request, 'reports/periodically-store-level-report.html', context)




# Reports by Zone
@login_required
def weeklyConsolidateReportByZone(request):
    zones = Zone.objects.all()
    sheet_heads = SheetHead.objects.all()
    zone = None
    weeks = None
    
    if request.method == 'GET':
        year = request.GET.get('year')
        zone_id = request.GET.get('zone_id')
        if zone_id:
            zone = get_object_or_404(Zone, id=zone_id)
        if year:
            weeks = Week.objects.filter(year=year)
        
    
    context = {
        'year' : year,
        'zones' : zones,
        'sheet_heads' : sheet_heads,
        'zone_id' : zone_id,
        'zone' : zone,
        'weeks' : weeks,
    }
    return render(request, 'reports/weekly-by-zone-report.html', context)


@login_required
def periodicallyConsolidateReportByZone(request):
    zones = Zone.objects.all()
    sheet_heads = SheetHead.objects.all()
    zone = None
    periods = None
    
    if request.method == 'GET':
        year = request.GET.get('year')
        zone_id = request.GET.get('zone_id')
        if zone_id:
            zone = get_object_or_404(Zone, id=zone_id)
        if year:
            periods = Period.objects.filter(year=year)
    
    context = {
        'year' : year,
        'zones' : zones,
        'sheet_heads' : sheet_heads,
        'zone_id' : zone_id,
        'zone' : zone,
        'periods' : periods,
    }
    return render(request, 'reports/periodically-by-zone-report.html', context)


@login_required
def addBudget(request):
    year = datetime.today().year
    years = [datetime.today().year-5 + index for index in range(10)]
    weeks = Week.objects.filter(year=year)
    stores = Store.objects.all()
    sheet_heads = SheetHead.objects.all()
    
    year = request.POST.get('year')
    weeks_inputted = request.POST.getlist('week')
    stores_inputted = request.POST.getlist('store')
    amounts = request.POST.getlist('budget')
    
    
    for i in range(len(weeks_inputted)):
        
        for j in range(len(stores_inputted)):
            budget = Budget.objects.create(
                year = year,
                week = Week.objects.get(id=weeks_inputted[i]),
                store = Store.objects.get(id=stores_inputted[j])
            )
        
            for k in range(len(sheet_heads)):
                BudgetDetail.objects.create(
                    budget = budget,
                    sheet_head = sheet_heads[k],
                    amount = amounts[k]
                )
    
    messages.success(request, f'Budget added successfully for {len(stores_inputted)} stores.')
    
    
    
    context = {
        'years' : years, 
        'weeks' : weeks,
        'stores' : stores,
        'sheet_heads' : sheet_heads,
    }
    return render(request, 'add-budget.html', context)


@login_required
def budgets(request):
    budgets = Budget.objects.all().order_by('year')
    
    context = {
        'budgets' : budgets,
    }
    return render(request, 'budgets.html', context)




# Charts Views

@login_required
def yearlyReportByStoreChartAjax(request):
    year = datetime.today().year
    head = SheetHead.objects.last()
    totals = []
    labels = []
    stores = Store.objects.all()
    
    for i in stores:
        labels.append(i.name)
        total = WeeklyConsolidateDetail.objects.filter(consolidate__year=year, head=head, consolidate__store=i).aggregate(total=Sum('amount'))['total']
        totals.append(total)
    
    
    
    data = {
        'labels' : labels,
        'totals' : totals,
    }
    return JsonResponse(data)


@login_required
def yearlyReportByHeadsChartAjax(request):
    year = datetime.today().year
    totals = []
    labels = []
    heads = SheetHead.objects.all()
    
    for i in heads:
        labels.append(i.name)
        total = WeeklyConsolidateDetail.objects.filter(consolidate__year=year, head=i).aggregate(total=Sum('amount'))['total']
        totals.append(total)
    
    
    
    data = {
        'labels' : labels,
        'totals' : totals,
    }
    return JsonResponse(data)


@login_required
def weeklyReportOfCurrentYearChartAjax(request):
    year = datetime.today().year
    head = SheetHead.objects.last()
    weeks = Week.objects.filter(year=year)
    labels = []
    totals = []
    
    for i in weeks:
        labels.append(i.name)
        total = WeeklyConsolidateDetail.objects.filter(consolidate__year = year, head=head, consolidate__week=i).aggregate(total=Sum('amount'))['total']  
        totals.append(total)
    
    data = {
        'labels' : labels,
        'totals' : totals,
    }
    return JsonResponse(data)


@login_required
def periodicReportOfCurrentYearChartAjax(request):
    year = datetime.today().year
    head = SheetHead.objects.last()
    periods = Period.objects.filter(start_week__year=year, end_week__year=year)
    labels = []
    totals = []
    
    for i in periods:
        labels.append(i.name)
        total = WeeklyConsolidateDetail.objects.filter(consolidate__year=year, head = head, 
                                                    consolidate__week__start_date__gte = i.start_week.start_date,
                                                    consolidate__week__end_date__lte = i.end_week.end_date,
                                                    ).aggregate(total=Sum('amount'))['total'] 
        
        totals.append(total) 
        
    
    data = {
        'labels' : labels,
        'totals' : totals,
    }
    return JsonResponse(data)