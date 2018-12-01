from django.conf.urls import url

from apps.goods.views import index, detail, category
from django.views.decorators.cache import cache_page

# 把主页设置到缓存中

urlpatterns = [
    url(r'^$', cache_page(3600)(index), name="首页"),
    url(r'^(?P<id>\d+).html/$', detail, name="商品详情"),
    url(r'^category/(?P<c_id>\d+)/(?P<order>\d)/$', category, name="超市"),
]
