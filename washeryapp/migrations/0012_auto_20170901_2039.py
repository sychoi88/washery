# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-01 20:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('washeryapp', '0011_driver_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='WayPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=500)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='washeryapp.Customer')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='washeryapp.Invoice')),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='waypoints', to='washeryapp.Route')),
            ],
        ),
        migrations.RemoveField(
            model_name='stop',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='stop',
            name='invoice',
        ),
        migrations.RemoveField(
            model_name='stop',
            name='route',
        ),
        migrations.DeleteModel(
            name='Stop',
        ),
    ]