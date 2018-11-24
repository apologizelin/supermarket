from django.conf.urls import url

from apps.goods.views import index, detail, category

urlpatterns = [
    url(r'^$', index, name="首页"),
    url(r'^detail/$', detail, name="商品详情"),
    url(r'^category/$', category, name="超市"),
]
