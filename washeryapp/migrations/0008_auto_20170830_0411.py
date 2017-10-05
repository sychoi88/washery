# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-30 04:11
from __future__ import unicode_literals

from django.db import migrations, models
import washeryapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('washeryapp', '0007_auto_20170824_0419'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='pieces',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='invoice',
            name='ready_by',
            field=models.DateTimeField(default=washeryapp.models.Invoice.two_day_hence),
        ),
        migrations.AddField(
            model_name='invoicedetail',
            name='piece_count',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]