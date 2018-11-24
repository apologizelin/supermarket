from django.contrib import admin

from apps.goods.models import LunBo, Active, AreaGoods, Produce, Assortment, Good, Goodsku, GoodPic, Comment


class GoodskuInline(admin.TabularInline):
    model = GoodPic
    extra = 2


@admin.register(LunBo)
class LunBoAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "goods_sku", "pic_url", "order"]
    list_display_links = ["id", "name", "goods_sku", "pic_url", "order"]


@admin.register(Active)
class ActiveAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "pic", "url"]
    list_display_links = ["id", "name", "pic", "url"]


@admin.register(AreaGoods)
class AreaGoodsAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "script", "order", "is_sale"]
    list_display_links = ["id", "name", "script", "order", "is_sale"]


@admin.register(Produce)
class ProduceAdmin(admin.ModelAdmin):
    list_display = ["id", "area_id", "goods_id"]
    list_display_links = ["id", "area_id", "goods_id"]


@admin.register(Assortment)
class AssortmentAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "introduce"]
    list_display_links = ["id", "name", "introduce"]


@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "detail"]
    list_display_links = ["id", "name", "detail"]


@admin.register(Goodsku)
class GoodskuAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "introduce", "unit", "price", "stock", "sale_num", "show_logo", "isGround",
                    "assortment_id", "good_id"]
    list_display_links = ["id", "name", "introduce", "unit", "price", "stock", "sale_num", "show_logo",
                          "isGround", "assortment_id", "good_id"]
    inlines = [GoodskuInline]


@admin.register(GoodPic)
class GoodPicAdmin(admin.ModelAdmin):
    list_display = ["id", "pic_url", "good_id"]
    list_display_links = ["id", "pic_url", "good_id"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "parent"]
    list_display_links = ["id", "name", "parent"]
