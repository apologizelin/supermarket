# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-30 15:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20181127_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraddress',
            name='hproper',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='市'),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Users', verbose_name='用户id'),
        ),
    ]
