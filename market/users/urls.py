from django.conf.urls import url

from users.views import register

urlpatterns = [
    url(r'^register/$', register, name="注册")
]
