# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-30 15:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allorder', '0003_auto_20181130_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='comment',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='备注说明'),
        ),
    ]
