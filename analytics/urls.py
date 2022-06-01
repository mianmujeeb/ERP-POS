from django.urls import path
from .views import *


urlpatterns = [
    path('', login, name='login'),
    path('logout', logout, name='logout'),
    path('dashboard', dashboard, name='dashboard'),
    
    path('managers', managers, name='managers'),
    path('manager/add', addManager, name='add-manager'),
    path('manager/update/<int:pk>', updateManager, name='update-manager'),
    path('manager/delete/<int:pk>', deleteManager, name='delete-manager'),
    
    path('stores', stores, name='stores'),
    path('store/add', addStore, name='add-store'),
    path('store/update/<int:pk>', updateStore, name='update-store'),
    path('store/delete/<int:pk>', deleteStore, name='delete-store'),
    
    path('zones', zones, name='zones'),
    
    path('sheetHeads', sheetHeads, name='sheet-heads'),
    
    
    path('weeks&Periods', weeksSetting, name='weeks'),
    path('week/update/<int:pk>', updateWeek, name='update-week'),
    path('weeksFilterAjax', filterWeeksAjax, name='weeks-filter-ajax'),
    
    path('weeklyconsolidates', consolidates, name='consolidates'),
    path('weeklyconsolidate/detail/<str:store_name>', consolidateDetail, name='consolidate-details'),
    path('weeklyconsolidate/complete_detail', consolidateDetailsDetails, name='consolidate-complete-detail'),
    
    path('weeklyconsolidates/years', consolidateYears, name='consolidate-years'),
    path('weeklyconsolidates/years/<int:year>', consolidateByYears, name='consolidate-by-years'),
    
    path('weeklyconsolidate/add', addConsolidate, name='add-consolidate'),
    
    path('budgets', budgets, name='budgets'),
    path('budget/add', addBudget, name='add-budget'),
    
    
    
    # Reports
    
    # Consolidated
    path('yearly-consolidate-report', yearlyConsolidateReport, name='yearly-consolidate-report'),
    path('weekly-consolidate-report', weeklyConsolidateReport, name='weekly-consolidate-report'),
    path('periodically-consolidate-report', periodicallyConsolidateReport, name='periodically-consolidate-report'),
    
    # By manager
    path('weekly-by-manager-report', weeklyConsolidateReportByManager, name='weekly-by-manager-report'),
    path('periodically-by-manager-report', periodicallyConsolidateReportByManager, name='periodically-by-manager-report'),
    
    #Bu Zone
    path('weekly-by-zone-report', weeklyConsolidateReportByZone, name='weekly-by-zone-report'),
    path('periodically-by-zone-report', periodicallyConsolidateReportByZone, name='periodically-by-zone-report'),
    
    # Store Level
    path('weekly-consolidate-report-by-store', weeklyConsolidateReportByStore, name='weekly-store-level-report'),
    path('periodically-consolidate-report-by-store', periodicallyConsolidateReportByStore, name='periodically-store-level-report'),
    
    
    
    
    # Charts URLS
    path('yearlyReportByStoreAjax', yearlyReportByStoreChartAjax, name='report-by-store-chart-ajax'),
    
    path('yearlyReportByHeadsAjax', yearlyReportByHeadsChartAjax, name='report-by-heads-chart-ajax'),
    
    path('periodicReportOfCurrentYearChartAjax', periodicReportOfCurrentYearChartAjax, name='report-by-periods-chart-ajax'),
    
    path('weeklyReportOfCurrentYearChartAjax', weeklyReportOfCurrentYearChartAjax, name='report-by-weeks-chart-ajax'),
    
]