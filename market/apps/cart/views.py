from django.shortcuts import render
from django_redis import get_redis_connection

from apps.goods.models import Goodsku


def cart(request):
    # 创建redis连接
    # r = get_redis_connection("default")
    # id = r.keys("")
    # # 根据redis中商品信息,从数据库中获取数据
    # goods = Goodsku.objects.filter(isDelete=False, isGround=True, pk=id)
    # 渲染页面
    # context = {
    #     "goods": goods
    # }
    return render(request, "cart/shopcart.html")
