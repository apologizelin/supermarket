from django.conf.urls import url

from apps.users.views import register, load, member, infor

urlpatterns = [
    url(r'^register/$', register, name="注册"),
    url(r'^load/$', load, name="登陆"),
    url(r'^member/$', member, name="个人中心"),
    url(r'^infor/$', infor, name="个人资料"),
]
