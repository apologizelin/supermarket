# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-25 14:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('isDelete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('pay_name', models.CharField(max_length=20, verbose_name='支付方式')),
            ],
            options={
                'verbose_name': '支付方式',
                'verbose_name_plural': '支付方式',
            },
        ),
        migrations.CreateModel(
            name='Transport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('isDelete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('name', models.CharField(max_length=20, verbose_name='配送方式')),
                ('money', models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='金额')),
            ],
            options={
                'verbose_name': '配送方式',
                'verbose_name_plural': '配送方式',
            },
        ),
    ]
