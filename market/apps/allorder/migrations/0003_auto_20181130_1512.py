# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-30 15:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20181130_1512'),
        ('goods', '0006_auto_20181125_1441'),
        ('allorder', '0002_auto_20181127_1506'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('isDelete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('good_num', models.IntegerField(default=0, verbose_name='商品数量')),
                ('good_price', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
            ],
            options={
                'verbose_name': '订单商品表',
                'verbose_name_plural': '订单商品表',
                'db_table': 'ordergoods',
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('isDelete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('order_num', models.CharField(max_length=100, verbose_name='订单编号')),
                ('order_money', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='订单金额')),
                ('name', models.CharField(max_length=100, verbose_name='收货人')),
                ('phone', models.CharField(max_length=100, verbose_name='收货人电话')),
                ('address', models.CharField(max_length=200, verbose_name='订单地址id')),
                ('status', models.SmallIntegerField(choices=[(0, '代付款'), (1, '代发货'), (2, '待收货'), (3, '待评价'), (4, '已完成')], default=0, verbose_name='订单状态')),
                ('transport', models.CharField(max_length=50, verbose_name='运输方式')),
                ('transport_price', models.CharField(max_length=50, verbose_name='运输价格')),
                ('order_amount', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='商品总价')),
                ('fact_money', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='实际支付')),
            ],
            options={
                'verbose_name': '订单信息表',
                'verbose_name_plural': '订单信息表',
                'db_table': 'orders',
            },
        ),
        migrations.AlterModelOptions(
            name='transport',
            options={'verbose_name': '运输方式', 'verbose_name_plural': '运输方式'},
        ),
        migrations.AddField(
            model_name='payment',
            name='img',
            field=models.ImageField(default='', upload_to='pay/', verbose_name='支付方式图'),
        ),
        migrations.AddField(
            model_name='orders',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='allorder.Payment', verbose_name='付款方式'),
        ),
        migrations.AddField(
            model_name='orders',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Users', verbose_name='用户id'),
        ),
        migrations.AddField(
            model_name='ordergoods',
            name='order_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='allorder.Orders', verbose_name='订单id'),
        ),
        migrations.AddField(
            model_name='ordergoods',
            name='sku_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.Goodsku', verbose_name='商品id'),
        ),
    ]
