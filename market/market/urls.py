"""market URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # 全文搜索框架
    url(r'^search/', include('haystack.urls')),
    # 上传部件自动调用的上传地址
    url(r'^ckeditor/', include("ckeditor_uploader.urls")),
    url(r'^users/', include("apps.users.urls", namespace="users")),  # 用户
    url(r'', include("apps.goods.urls", namespace="goods")),  # 商品
    url(r'^cart/', include("apps.cart.urls", namespace="cart")),  # 购物车
    url(r'^allorder/', include("apps.allorder.urls", namespace="allorder")),  # 订单
]
