# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-03 01:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('washeryapp', '0017_auto_20170902_2043'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='completed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='route',
            name='started_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
