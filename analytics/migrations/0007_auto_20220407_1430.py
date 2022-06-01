# Generated by Django 3.2.12 on 2022-04-07 09:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0006_auto_20220407_1219'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weeklyconsolidate',
            name='net_sale_amount',
        ),
        migrations.RemoveField(
            model_name='weeklyconsolidate',
            name='net_sale_percentage',
        ),
        migrations.CreateModel(
            name='WeeklyConsolidateDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=1000)),
                ('consolidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consolidate_detail', to='analytics.weeklyconsolidate')),
                ('head', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analytics.sheethead')),
            ],
            options={
                'verbose_name': 'Weekly Consolidate Detail',
                'verbose_name_plural': 'Weekly Consolidate Details',
            },
        ),
    ]