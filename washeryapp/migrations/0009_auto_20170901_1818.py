# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-01 18:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('washeryapp', '0008_auto_20170830_0411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='ready_by',
            field=models.DateTimeField(),
        ),
    ]
