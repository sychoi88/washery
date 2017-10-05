# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-02 03:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('washeryapp', '0023_auto_20171002_0317'),
    ]

    operations = [
        migrations.AddField(
            model_name='cleaner',
            name='latitude',
            field=models.DecimalField(decimal_places=6, default=33.348126, max_digits=9),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cleaner',
            name='longitude',
            field=models.DecimalField(decimal_places=6, default=-111.757127, max_digits=9),
            preserve_default=False,
        ),
    ]
