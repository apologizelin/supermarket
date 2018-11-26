from django.conf.urls import url

from apps.cart.views import Addcart, cart, CartAdd, CartReduce

urlpatterns = [
    url(r'^addCart/$', Addcart.as_view(), name="addCart"),  # 商品详情页添加购物车
    url(r'^CartADD/$', CartAdd.as_view(), name="CartAdd"),  # 购物车添加
    url(r'^CartReduce/$', CartReduce.as_view(), name="CartReduce"),  # 购物车减少
    url(r'^$', cart, name="cart"),
]
