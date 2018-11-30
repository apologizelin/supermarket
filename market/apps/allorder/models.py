from django.db import models

from db.base_model import BaseModel


class Payment(BaseModel):
    """支付方式"""
    pay_name = models.CharField(max_length=20, verbose_name='支付方式')
    img = models.ImageField(upload_to="pay/", default="", verbose_name="支付方式图")

    class Meta:
        db_table = "payment"
        verbose_name = "支付方式"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.pay_name


class Transport(BaseModel):
    """运输方式"""
    name = models.CharField(max_length=20, verbose_name='配送方式')
    money = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name='金额')

    class Meta:
        db_table = "transport"
        verbose_name = "运输方式"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Orders(BaseModel):
    """订单信息表"""
    status_choices = (
        (0, "代付款"),
        (1, "代发货"),
        (2, "待收货"),
        (3, "待评价"),
        (4, "已完成"),
    )
    user_id = models.ForeignKey(to="users.Users", verbose_name="用户id")
    order_num = models.CharField(max_length=100, verbose_name="订单编号", unique=True)
    name = models.CharField(max_length=100, verbose_name="收货人")
    phone = models.CharField(max_length=100, verbose_name="收货人电话")
    address = models.CharField(max_length=200, verbose_name="订单地址")
    status = models.SmallIntegerField(choices=status_choices, default=0, verbose_name="订单状态")
    transport = models.CharField(max_length=50, verbose_name="运输方式")
    transport_price = models.CharField(max_length=50, verbose_name="运输价格")
    payment = models.ForeignKey(to="Payment", null=True, blank=True, verbose_name="付款方式")
    order_amount = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name="商品总价")
    fact_money = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name="实际支付")
    comment = models.CharField(max_length=200, null=True, blank=True, verbose_name="备注说明")

    class Meta:
        db_table = "orders"
        verbose_name = "订单信息表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class OrderGoods(BaseModel):
    """订单商品表"""
    order_id = models.ForeignKey(to="Orders", verbose_name="订单id")
    sku_id = models.ForeignKey(to="goods.Goodsku", verbose_name="商品id")
    good_num = models.IntegerField(default=0, verbose_name="商品数量")
    good_price = models.DecimalField(default=0, max_digits=9, decimal_places=2)

    class Meta:
        db_table = "ordergoods"
        verbose_name = "订单商品表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order_id.name
