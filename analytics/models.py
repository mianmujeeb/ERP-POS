from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Manager(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    
    class Meta:

        verbose_name = 'Manager'
        verbose_name_plural = 'Managers'

    def __str__(self):
        return self.first_name + " " + self.last_name


    

class SheetHead(models.Model):
    name = models.CharField(max_length=100)
    order = models.IntegerField(null=True, blank=True)

    class Meta:

        verbose_name = 'Sheet Head'
        verbose_name_plural = 'Sheet Heads'

    def __str__(self):
        return self.name
    
    
    
class Zone(models.Model):
    name = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="zone_added_by")

    class Meta:

        verbose_name = 'Zone'
        verbose_name_plural = 'Zones'

    def __str__(self):
        return self.name
    
    
class Store(models.Model):
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="store_added_by")

    class Meta:

        verbose_name = 'Store'
        verbose_name_plural = 'Stores'

    def __str__(self):
        return self.name





class Week(models.Model):
    name = models.CharField(max_length=150)
    year = models.CharField(max_length=10)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:

        verbose_name = 'Week'
        verbose_name_plural = 'Weeks'

    def __str__(self):
        return self.name + ' (' + self.year + ')'
    
    
    
class Period(models.Model):
    name = models.CharField(max_length=100)
    year = models.CharField(max_length=10)
    start_week = models.ForeignKey(Week, on_delete=models.CASCADE, related_name="period_start_week")
    end_week = models.ForeignKey(Week, on_delete=models.CASCADE, related_name="period_end_week")

    class Meta:

        verbose_name = 'Period'
        verbose_name_plural = 'Periods'

    def __str__(self):
        return self.start_week.name + " " + self.end_week.name + " (" + str(self.year) + ")"




class WeeklyConsolidate(models.Model):
    year = models.IntegerField()
    week = models.ForeignKey(Week, on_delete=models.CASCADE, related_name='week_weekly_consolidate')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_weekly_consolidate')
    
    class Meta:

        verbose_name = 'Weekly Consolidate'
        verbose_name_plural = 'Weekly Consolidate'

    def __str__(self):
        return self.store.name + ' ' + str(self.year) + ' ' + self.week.name


class WeeklyConsolidateDetail(models.Model):
    consolidate = models.ForeignKey(WeeklyConsolidate, on_delete=models.CASCADE, related_name='consolidate_detail')
    head = models.ForeignKey(SheetHead, on_delete=models.CASCADE)
    amount = models.CharField(max_length=1000)

    class Meta:

        verbose_name = 'Weekly Consolidate Detail'
        verbose_name_plural = 'Weekly Consolidate Details'

    def __str__(self):
        return self.consolidate.store.name




class Budget(models.Model):
    year = models.IntegerField()
    week = models.ForeignKey(Week, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='budgets')
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:

        verbose_name = 'Budget'
        verbose_name_plural = 'Budgets'

    def __str__(self):
        return str(self.year) + str(self.store)
    
    
class BudgetDetail(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name="budget_detail")
    sheet_head = models.ForeignKey(SheetHead, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=1000)

    class Meta:

        verbose_name = 'Budget Detail'
        verbose_name_plural = 'Budget Details'

    def __str__(self):
        return str(self.budget.year) + str(self.budget.store)

