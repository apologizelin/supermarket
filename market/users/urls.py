from django.conf.urls import url

from users.views import register, load

urlpatterns = [
    url(r'^register/$', register, name="注册"),
    url(r'^load/$', load, name="登陆"),
]
