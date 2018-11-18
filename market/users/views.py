import hashlib

from django.shortcuts import render, redirect

# Create your views here.
from users.models import Users


def index(request):
    return render(request, "users/index.html")


def register(request):
    if request.method == "GET":
        # 显示注册页面
        return render(request, "users/reg.html")
    else:
        # 注册并保持到数据库
        datas = request.POST
        username = datas.get("username")
        pwd = datas.get("pwd")
        ha = hashlib.md5(pwd.encode("utf-8"))
        pwd = ha.hexdigest()
        user = Users.objects.filter(username=username)
        if user:
            return render(request, "users/reg.html")
        else:
            Users.objects.create(username=username, pwd=pwd)
            return redirect("users:登陆")


def load(request):
    if request.method == "GET":
        return render(request, "users/login.html")
    else:
        data = request.POST
        username = data.get("username")
        pwd = data.get("pwd")
        try:
            user = Users.objects.get(username=username)
        except Users.MultipleObjectsReturned:
            # 获取多个记录
            return redirect("users:登陆")
        except Users.DoesNotExist:
            return redirect("users:登陆")
        ha = hashlib.md5(pwd.encode("utf-8"))
        pwd = ha.hexdigest()
        # 验证账户
        if pwd == user.pwd:
            request.session["ID"] = user.id
            request.session["username"] = user.username
            return redirect("users:首页")
        else:
            return redirect("users:登陆")
