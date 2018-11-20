# 登录验证装饰器
import hashlib

from django.shortcuts import redirect


# 封装验证session的方法
from market import settings


def verify_login_required(func):
    """
    :param func: 传入的函数
    :return:
    """  # 登陆验证器

    def verify(request, *args, **kwargs):
        # 判断session中是否有ID,如果没有说明没有登录，请登录
        if request.session.get("ID") is None:
            # 配置文件中获取登录的URL地址
            return redirect("users:login")
        else:
            # 返回被调用函数
            return func(request, *args, **kwargs)

    return verify


# 加密方法
def set_password(password):
    # 新的加密字符串
    new_password = "{}{}".format(password, settings.SECRET_KEY)
    h = hashlib.md5(new_password.encode('utf-8'))
    return h.hexdigest()


# 登陆保存session的方法
def login(request, user):
    # 将用户id和手机号码,保存到session中
    request.session['ID'] = user.pk
    request.session['username'] = user.username
    # request.session['head'] = user.head
