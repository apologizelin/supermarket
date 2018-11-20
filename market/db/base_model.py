from django.db import models
from django.utils.decorators import method_decorator
from django.views import View

from apps.users.helper import verify_login_required


class BaseModel(models.Model):
    """基础模型类"""
    time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    update = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    isDelete = models.BooleanField(default=False, verbose_name="是否删除")

    class Meta:
        # 设置抽象的类
        abstract = True


class BaseVerifyView(View):
    """
        基础类视图，用于验证是否登录
    """

    @method_decorator(verify_login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(BaseVerifyView, self).dispatch(request, *args, **kwargs)
