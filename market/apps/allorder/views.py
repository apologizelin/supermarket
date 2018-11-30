from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from apps.allorder.models import Transport, Orders, OrderGoods
from apps.goods.models import Goodsku
from apps.users.forms import AddressForm, EditaddressForm
from apps.users.models import UserAddress
from db.base_model import BaseVerifyView
from django_redis import get_redis_connection
from datetime import datetime
import random


def allorder(request):
    return render(request, "allorder/allorder.html")


# 管理收货地址页面
def gladdress(request):
    data = UserAddress.objects.filter(isDelete=False).order_by("-isDefault")
    context = {
        "data": data
    }
    return render(request, "allorder/gladdress.html", context)


# 增加收货地址页面
def address(request):
    if request.method == "POST":
        data = request.POST.dict()
        user_id = request.session.get("ID")
        data["user_id"] = user_id
        form = AddressForm(data)
        # print(data.get("isDefault"))
        if form.is_valid():
            clean_data = form.cleaned_data
            UserAddress.objects.create(user_id=user_id, **clean_data)
            return redirect("allorder:gladdress")
        else:
            # 验证失败,返回错误信息
            context = {
                "form": form,
            }
            return render(request, "allorder/address.html", context)
    else:
        return render(request, "allorder/address.html")


# 编辑收货地址
class EditAddress(BaseVerifyView):

    def get(self, request, id):
        user_id = request.session.get("ID")
        try:
            address = UserAddress.objects.get(user_id=user_id, pk=id)
        except UserAddress.DoesNotExist:
            return redirect("allorder:address")
        context = {
            "address": address
        }
        return render(request, "allorder/editAddress.html", context)

    def post(self, request, id):
        data = request.POST.dict()
        user_id = request.session.get("ID")
        data["user_id"] = user_id
        form = EditaddressForm(data)
        if form.is_valid():
            clean_data = form.cleaned_data
            id = data.get('id')
            UserAddress.objects.filter(user_id=user_id, pk=id).update(**clean_data)
            return redirect("allorder:gladdress")
        else:
            # 验证失败,返回错误信息
            context = {
                "form": form,
                "address": data
            }
            return render(request, "allorder/editAddress.html", context)


# 删除收货地址
def delAddress(request):
    if request.method == "POST":
        id = request.POST.get("id")
        user_id = request.session.get("ID")
        UserAddress.objects.filter(user_id=user_id, pk=id).update(isDelete=True)
        return JsonResponse({"code": 0, "msg": "成功"})
    else:
        return JsonResponse({"code": 1, "errmsg": "参数错误"})


# 设置默认收货地址
def defaAddress(request):
    if request.method == "POST":
        id = request.POST.get("id")
        user_id = request.session.get("ID")
        UserAddress.objects.all().update(isDefault=False)
        UserAddress.objects.filter(user_id=user_id, pk=id).update(isDefault=True)
        return JsonResponse({"code": 0, "msg": "成功"})
    else:
        return JsonResponse({"code": 1, "errmsg": "参数错误"})


# 确认订单页面
class Tureorder(View):
    # 回显确认订单页面
    def get(self, request):
        # 判断是否登录
        user_id = request.session.get("ID")
        if not user_id:
            return redirect("users:login")
        # 获取收货地址对象
        address = UserAddress.objects.filter(user_id=user_id, isDelete=False).order_by("-isDefault").first()
        # 获取商品sku_id
        sku_ids = request.GET.getlist("sku_id")
        # 如果没有,跳转到购物车
        if len(sku_ids) == 0:
            return redirect("cart:cart")
        # 转为整数
        try:
            sku_ids_list = [int(sku_id) for sku_id in sku_ids]
        except:
            return redirect("cart:cart")

        # 准备reids
        r = get_redis_connection("default")
        cart_key = "cart_key_{}".format(user_id)

        # 获取商品信息
        goodskus = []
        total_price = 0
        for sku_id in sku_ids_list:
            goods = Goodsku.objects.get(pk=sku_id)
            # 获取购物车中的数量
            count = int(r.hget(cart_key, sku_id))
            goods.count = count
            # 计算总价
            total_price += goods.price * count
            goodskus.append(goods)

        # 运输方式,价格升序
        transport = Transport.objects.filter(isDelete=False).order_by("money")

        context = {
            "address": address,
            "goodskus": goodskus,
            "total_price": total_price,
            "transport": transport,
        }

        return render(request, "allorder/tureorder.html", context)

    def post(self, request):
        # 提交订单数据
        # 判断用户是否登录
        user_id = request.session.get("ID")
        if not user_id:
            return JsonResponse({"code": 1, "errmsg": "没有登录!"})
        # 获取数据
        comment = request.POST.get("comment")
        address_id = request.POST.get("address_id")
        transport_id = request.POST.get("transport")
        sku_ids = request.POST.getlist("sku_id")
        # 判断参数是否存在
        if not all([address_id, transport_id, sku_ids]):
            return JsonResponse({"code": 2, "errmsg": "参数错误!"})
        # 判断是否为整数
        try:
            address_id = int(address_id)
            transport_id = int(transport_id)
            sku_ids_int = [int(sku_id) for sku_id in sku_ids]
        except:
            return JsonResponse({"code": 3, "errmsg": "参数错误!"})
        # 判断收货地址和运输方式必须存在
        try:
            address = UserAddress.objects.get(pk=address_id, isDelete=False)
        except UserAddress.DoesNotExist:
            return JsonResponse({"code": 4, "errmsg": "收货地址不存在!"})
        try:
            transport = Transport.objects.get(pk=transport_id, isDelete=False)
        except Transport.DoesNotExist:
            return JsonResponse({"code": 5, "errmsg": "收货地址不存在!"})
        # 将数据保存到订单表中
        # 准备订单编号
        order_num = "{}{}{}".format(datetime.today().strftime("%Y%m%d%H%M%S"), user_id, random.randint(10000, 99999))
        # 准备详细地址
        detail = "{} {} {} {}".format(address.hcity, address.hproper, address.harea, address.brief)
        order = Orders.objects.create(
            user_id_id=user_id,
            order_num=order_num,
            name=address.username,
            phone=address.phone,
            address=detail,
            transport=transport.name,
            transport_price=transport.money,
            comment=comment
        )
        # 连接redis
        cart_key = "cart_key_{}".format(user_id)
        r = get_redis_connection("default")

        # 保存商品总价
        order_amount = 0

        # 遍历商品id
        for sku in sku_ids_int:
            try:
                goods = Goodsku.objects.get(pk=sku, isDelete=False, isGround=True)
            except Goodsku.DoesNotExist:
                return JsonResponse({"code": 6, "errmsg": "商品不存在!"})
            # 获取redis中商品数量
            try:
                count = int(r.hget(cart_key, sku))
            except:
                return JsonResponse({"code": 7, "errmsg": "参数错误!"})
            # 判断库存是否足够
            if goods.stock < count:
                return JsonResponse({"code": 8, "errmsg": "商品库存不足!"})
            # 保存到订单商品表
            OrderGoods.objects.create(order_id=order, sku_id=goods, good_num=count, good_price=goods.price)
            # 改变销量与库存
            goods.stock -= count
            goods.sale_num += count
            goods.save()
            # 计算总价
            order_amount += goods.price * count
        # 计算总金额
        try:
            order.order_amount = order_amount
            order.save()
        except:
            return JsonResponse({"code": 9, "errmsg": "保存总金额失败!"})
        # 删除购物车中的商品
        r.hdel(cart_key, *sku_ids_int)

        # 成功
        return JsonResponse({"code": 0, "msg": "成功!", "order_num": order_num})


# 支付订单页面
class Order(BaseVerifyView):
    def get(self, request):
        # 接受数据
        user_id = request.session.get("ID")
        order_num = request.GET.get("order_num")
        try:
            order = Orders.objects.get(order_num=order_num, user_id=user_id)
        except Orders.DoesNotExist:
            return redirect("cart:cart")
        # 计算总价
        total = float(order.order_amount) + float(order.transport_price)
        url = ""
        context = {
            "order": order,
            "total": total,
            "url": url
        }
        return render(request, "allorder/order.html", context)

    def post(self, request):
        pass
