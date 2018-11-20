import hashlib

from django.shortcuts import render, redirect

# Create your views here.
from apps.users.forms import RegForm, LoadForm
from apps.users.models import Users, Infor


def register(request):
    if request.method == "GET":
        # 显示注册页面
        return render(request, "users/reg.html")
    else:
        datas = request.POST
        form = RegForm(datas)
        # 表单验证
        if form.is_valid():
            datas = form.cleaned_data
            # 注册并保存到数据库
            username = datas.get("username")
            pwd = datas.get("password")
            ha = hashlib.md5(pwd.encode("utf-8"))
            pwd = ha.hexdigest()
            user = Users.objects.filter(username=username)
            if user:
                return render(request, "users/reg.html")
            else:
                Users.objects.create(username=username, password=pwd)
                return redirect("users:登陆")
        else:
            context = {
                "errors": form.errors,
                "datas": datas
            }
            return render(request, "users/reg.html", context)


def load(request):
    if request.method == "GET":
        return render(request, "users/login.html")
    else:
        data = request.POST
        form = LoadForm(data)
        # 表单验证
        if form.is_valid():
            data = form.cleaned_data
            username = data.get("username")
            pwd = data.get("password")
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
            if pwd == user.password:
                request.session["ID"] = user.id
                request.session["username"] = user.username
                return redirect("goods:首页")
            else:
                return redirect("users:登陆")
        else:
            context = {
                "errors": form.errors,
                "data": data
            }
            return render(request, "users/login.html", context)


def member(requset):
    username = requset.session.get("username")
    if username:
        context = {
            "username": username
        }
        return render(requset, "users/member.html", context)
    else:
        return redirect("users:登陆")


def infor(request):
    if request.method == "GET":
        id = request.session.get("ID")
        info = Infor.objects.get(num_id=id)
        context = {
            "info": info
        }
        return render(request, "users/infor.html", context)
    else:
        data = request.POST
        nickname = data.get("nickname")
        sex = data.get("sex")
        birthday = data.get("birthday")
        school = data.get("school")
        address = data.get("address")
        hometown = data.get("hometown")
        phone = data.get("phone")
        id = request.session.get("ID")
        Infor.objects.filter(num_id=id).update(nickname=nickname, sex=sex, birthday=birthday, school=school, address=address, hometown=hometown, phone=phone)
        context = {
            "info": data
        }
        return render(request, "users/infor.html", context)
