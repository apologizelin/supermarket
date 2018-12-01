from django.conf.urls import url

from apps.allorder.views import allorder, gladdress, address, delAddress, EditAddress, defaAddress, Tureorder, Order, \
    pay, success

urlpatterns = [
    url(r'^$', allorder, name="订单"),  # 订单管理
    url(r'^gladdress/$', gladdress, name="gladdress"),  # 管理收货地址页面
    url(r'^address/$', address, name="address"),  # 增加收货地址页面
    url(r'^editAddress/(?P<id>\d+)/$', EditAddress.as_view(), name="editAddress"),  # 编辑收货地址页面
    url(r'^delAddress/$', delAddress, name="delAddress"),  # 删除收货地址
    url(r'^defaAddress/$', defaAddress, name="defaAddress"),  # 设置为默认收货地址
    url(r'^tureorder/$', Tureorder.as_view(), name="tureorder"),  # 确认订单
    url(r'^order/$', Order.as_view(), name="order"),  # 展示付款
    url(r'^pay/$', pay, name="pay"),  # 发起支付
    url(r'^success/$', success, name="success")  # 支付成功
]
