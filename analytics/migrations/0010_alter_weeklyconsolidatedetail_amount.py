# Generated by Django 3.2.12 on 2022-04-07 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0009_alter_weeklyconsolidate_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weeklyconsolidatedetail',
            name='amount',
            field=models.CharField(max_length=1000),
        ),
    ]
