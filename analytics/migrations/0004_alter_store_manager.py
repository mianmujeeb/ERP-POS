# Generated by Django 3.2.12 on 2022-04-04 19:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0003_manager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analytics.manager'),
        ),
    ]