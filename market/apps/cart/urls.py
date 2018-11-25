from django.conf.urls import url

from apps.cart.views import cart

urlpatterns = [
    url(r'^$', cart, name="购物车")
]
