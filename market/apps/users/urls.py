from django.conf.urls import url

from apps.users.views import LoginView, RegisterView, MemberView, InfomationView, ForgetPassView, sendMsg

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name="login"),  # 登陆
    url(r'^register/$', RegisterView.as_view(), name="register"),  # 注册
    url(r'^forget/$', ForgetPassView.as_view(), name="forget"),  # 忘记密码
    url(r'^member/$', MemberView.as_view(), name="member"),  # 个人中心
    url(r'^info/$', InfomationView.as_view(), name="info"),  # 个人资料
    url(r'^send/$', sendMsg, name="sendMsg"),  # 发送短信
]
