from django.conf.urls import url

from apps.allorder.views import allorder

urlpatterns = [
    url(r'^$', allorder, name="订单")
]
