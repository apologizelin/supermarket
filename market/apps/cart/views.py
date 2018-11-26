from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django_redis import get_redis_connection

from apps.goods.models import Goodsku


# 详情页面商品添加到购物车
class Addcart(View):
    def get(self, request):
        return redirect("cart:cart")

    def post(self, request):
        # 判断用户是否登录
        user_id = request.session.get("ID")
        if user_id is None:
            # 没有登录
            return JsonResponse({"code": 1, "errmsg": "没有登录!"})
        num = request.POST.get("num")
        sku_id = request.POST.get("sku_id")
        # 判断参数是否正确
        try:
            num = int(num)
            sku_id = int(sku_id)
        except:
            return JsonResponse({"code": 2, "errmsg": "参数错误"})
        if num <= 0:
            return JsonResponse({"code": 3, "errmsg": "参数错误"})
        # 判断商品是否存在
        try:
            goods = Goodsku.objects.get(pk=sku_id)
        except Goodsku.DoesNotExist:
            return JsonResponse({"code": 4, "errmsg": "商品不存在"})
        # 判断商品是否超过库存
        if num > goods.stock:
            return JsonResponse({"code": 5, "errmsg": "库存不足"})
        # 保存数据到redis中
        r = get_redis_connection('default')
        cart_key = "cart_key_{}".format(user_id)
        r.hincrby(cart_key, sku_id, num)
        return JsonResponse({"code": 0, "msg": "成功"})


# 购物车商品添加
class CartAdd(View):
    def get(self, request):
        redirect("cart:cart")

    def post(self, request):
        # 判断用户是否登录
        user_id = request.session.get("ID")
        if user_id is None:
            # 没有登录
            return JsonResponse({"code": 1, "errmsg": "没有登录!"})
        num = request.POST.get("num")
        sku_id = request.POST.get("sku_id")
        # 判断参数是否正确
        try:
            num = int(num)
            sku_id = int(sku_id)
        except:
            return JsonResponse({"code": 2, "errmsg": "参数错误"})
        if num <= 0:
            return JsonResponse({"code": 3, "errmsg": "参数错误"})
        # 判断商品是否存在
        try:
            goods = Goodsku.objects.get(pk=sku_id)
        except Goodsku.DoesNotExist:
            return JsonResponse({"code": 4, "errmsg": "商品不存在"})
        # 判断商品是否超过库存
        if num > goods.stock:
            return JsonResponse({"code": 5, "errmsg": "库存不足"})
        # 保存数据到redis中
        r = get_redis_connection('default')
        cart_key = "cart_key_{}".format(user_id)
        r.hset(cart_key, sku_id, num)
        return JsonResponse({"code": 0, "msg": "成功"})


# 购物车商品减少
class CartReduce(View):
    def get(self, request):
        return redirect("cart:cart")

    def post(self, request):
        # 连接redis
        r = get_redis_connection('default')
        # 判断用户是否登录
        user_id = request.session.get("ID")
        if user_id is None:
            # 没有登录
            return JsonResponse({"code": 1, "errmsg": "没有登录!"})
        num = request.POST.get("num")
        sku_id = request.POST.get("sku_id")
        cart_key = "cart_key_{}".format(user_id)
        # 判断参数是否正确
        try:
            num = int(num)
            sku_id = int(sku_id)
        except:
            return JsonResponse({"code": 2, "errmsg": "参数错误"})
        if num <= 0 or num == None:
            r.hdel(cart_key, sku_id)
            return JsonResponse({"code": 3, "errmsg": "参数错误"})
        # 判断商品是否存在
        try:
            goods = Goodsku.objects.get(pk=sku_id)
        except Goodsku.DoesNotExist:
            return JsonResponse({"code": 4, "errmsg": "商品不存在"})
        # 判断商品是否超过库存
        if num > goods.stock:
            return JsonResponse({"code": 5, "errmsg": "库存不足"})
        # 保存数据到redis中
        r.hset(cart_key, sku_id, num)
        return JsonResponse({"code": 0, "msg": "成功"})


# 渲染购物车
def cart(request):
    user_id = request.session.get("ID")
    r = get_redis_connection("default")
    cart_key = "cart_key_{}".format(user_id)
    data = r.hgetall(cart_key)
    datas = []
    for sku_id, num in data.items():
        sku_id = int(sku_id)
        num = int(num)
        good = Goodsku.objects.get(pk=sku_id)
        good.num = num
        datas.append(good)
    context = {
        "data": datas,
    }
    return render(request, "cart/shopcart.html", context)
