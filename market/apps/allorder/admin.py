from django.contrib import admin

from apps.allorder.models import Payment, Transport


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["id", "pay_name"]
    list_display_links = ["id", "pay_name"]


@admin.register(Transport)
class TransportAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "money"]
    list_display_links = ["id", "name", "money"]
