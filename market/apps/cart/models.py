from django.db import models

from db.base_model import BaseModel


class Payment(BaseModel):
    """支付方式"""
    pay_name = models.CharField(max_length=20, verbose_name='支付方式')

    class Meta:
        verbose_name = "支付方式"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.pay_name


class Transport(BaseModel):
    """配送方式"""
    name = models.CharField(max_length=20, verbose_name='配送方式')
    money = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name='金额')

    class Meta:
        verbose_name = "配送方式"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
