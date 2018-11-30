from django.contrib import admin

from apps.allorder.models import Payment, Transport, Orders, OrderGoods


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["id", "pay_name", "img"]
    list_display_links = ["id", "pay_name", "img"]


@admin.register(Transport)
class TransportAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "money"]
    list_display_links = ["id", "name", "money"]


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "order_num", "order_amount", "name", "phone", "address", "status", "transport",
                    "transport_price", "payment", "fact_money"]
    list_display_links = ["id", "name", "order_num", "order_amount", "name", "phone", "address", "status",
                          "transport", "transport_price", "payment", "fact_money"]


@admin.register(OrderGoods)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ["id", "order_id", "sku_id", "good_num", "good_price"]
    list_display_links = ["id", "order_id", "sku_id", "good_num", "good_price"]
