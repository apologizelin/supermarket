# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-23 16:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goodsku',
            name='url',
        ),
        migrations.AlterField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.Goodsku', verbose_name='商品skuid'),
        ),
        migrations.AlterField(
            model_name='goodpic',
            name='pic_url',
            field=models.ImageField(upload_to='goods', verbose_name='图片地址'),
        ),
        migrations.AlterField(
            model_name='goodsku',
            name='logo_url',
            field=models.ImageField(default='', upload_to='goods', verbose_name='logo地址'),
        ),
    ]
