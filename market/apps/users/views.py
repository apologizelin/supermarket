import random
import re
import uuid

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from apps.users.forms import RegForm, LoadForm, RorgetForm, AddressForm
from apps.users.helper import set_password, login, verify_login_required, send_sms
from apps.users.models import Users, Infor, UserAddress
from django_redis import get_redis_connection
from db.base_model import BaseVerifyView


class RegisterView(View):
    """注册"""

    def get(self, request):
        return render(request, "users/reg.html")

    def post(self, request):
        datas = request.POST
        form = RegForm(datas)
        # 表单验证
        if form.is_valid():
            datas = form.cleaned_data
            # 注册并保存到数据库
            username = datas.get("username")
            pwd = datas.get("password")
            pwd = set_password(pwd)
            Users.objects.create(username=username, password=pwd)
            return redirect("users:login")
        else:
            # 验证失败,返回错误信息
            context = {
                "errors": form.errors,
                "datas": datas
            }
            return render(request, "users/reg.html", context)


def send_phone_code(request):
    """短信验证"""
    try:
        # 获取手机号码
        phone = request.GET.get('phone')
        # 验证手机号码格式
        phone_v = re.compile('^1[3-9]\d{9}$')
        rs = re.search(phone_v, phone)
        if rs:
            # 格式正确,生成随机验证码
            code = "".join([str(random.randint(0, 9)) for _ in range(4)])
            # 将验证码保存到redis中
            r = get_redis_connection("default")
            r.set(phone, code)
            r.expire(phone, 120)

            # 发送短信验证(注释后以便测试)
            print(code)
            # __business_id = uuid.uuid1()
            # # print(__business_id)
            # params = "{\"code\":\"%s\",\"product\":\"校园超市\"}" % code
            # # params = u'{"name":"wqb","code":"12345678","address":"bz","phone":"13000000000"}'
            # print(send_sms(__business_id, phone, "注册验证", "SMS_2245271", params))

            # 验证成功
            return {'ok': 1, 'code': 200}
        else:
            # 验证失败
            return {'ok': 0, 'code': 500, 'msg': '手机号码格式错误！'}
    except:
        # 没有获取到手机号
        return {'ok': 0, 'code': 500, 'msg': '短信验证码发送失败'}


# 短信发送 视图函数
def sendMsg(request):
    return JsonResponse(send_phone_code(request))


class LoginView(View):
    """登陆"""

    def get(self, request):
        # 创建登陆表单对象
        login_form = LoadForm()
        return render(request, "users/login.html", {'form': login_form})

    def post(self, request):
        data = request.POST
        form = LoadForm(data)
        # 表单验证
        if form.is_valid():
            # 验证成功后将登陆标识放到session中
            user = form.cleaned_data.get('user')
            # 调用登陆的方法,放在helper模块中的
            login(request, user)

            # 登陆成功返回之前页面
            next = request.GET.get("next")
            if next:
                return redirect(next)

            # 跳转到用户中心页面
            return redirect('users:member')
        else:
            context = {
                "errors": form.errors
            }
            return render(request, "users/login.html", context)


class ForgetPassView(View):
    def get(self, request):
        return render(request, "users/forgetpassword.html")

    def post(self, request):
        datas = request.POST
        form = RorgetForm(datas)
        # 表单验证
        if form.is_valid():
            datas = form.cleaned_data
            # 修改并保存到数据库
            username = datas.get("username")
            pwd = datas.get("password")
            pwd = set_password(pwd)
            Users.objects.filter(username=username).update(password=pwd)
            return redirect("users:login")
        else:
            # 验证失败,返回错误信息
            context = {
                "errors": form.errors,
                "datas": datas
            }
            return render(request, "users/forgetpassword.html", context)


class MemberView(BaseVerifyView):
    """个人中心"""

    def get(self, request):
        username = request.session.get("username")
        id = request.session.get("ID")
        data = Infor.objects.filter(num_id=id).first()
        print(data)
        context = {
            "username": username,
            "data": data
        }
        return render(request, "users/member.html", context)


class InfomationView(BaseVerifyView):
    """个人资料"""

    def get(self, request):
        id = request.session.get("ID")
        # 捕获异常,有数据就回显,没有数据则显示添加数据的提示信息
        try:
            info = Infor.objects.get(num_id=id)
        except:
            return render(request, "users/infor.html")
        context = {
            "info": info
        }
        return render(request, "users/infor.html", context)

    def post(self, request):
        # 获取post中表单提交的数据
        data = request.POST
        nickname = data.get("nickname")
        sex = data.get("sex")
        birthday = data.get("birthday")
        school = data.get("school")
        address = data.get("address")
        hometown = data.get("hometown")
        phone = data.get("phone")
        id = request.session.get("ID")
        # 获取头像地址
        head = request.FILES.get("head")
        # head = str(he)
        print(head)
        info = Infor.objects.filter(num_id=id).first()
        # 判断是否填写过个人资料,填写过再提交便做更新,否则创建
        if info:
            # Infor.objects.filter(num_id=id).update(head=head, nickname=nickname, sex=sex, birthday=birthday,
            #                                        school=school,
            #                                        address=address, hometown=hometown, phone=phone, num_id=id)
            if head:
                info.head = head
                info.nickname = nickname
                info.sex = sex
                info.birthday = birthday
                info.school = school
                info.address = address
                info.hometown = hometown
                info.phone = phone
                info.save()
            else:
                info.nickname = nickname
                info.sex = sex
                info.birthday = birthday
                info.school = school
                info.address = address
                info.hometown = hometown
                info.phone = phone
                info.save()
            return redirect("users:member")
        else:
            Infor.objects.create(head=head, nickname=nickname, sex=sex, birthday=birthday, school=school,
                                 address=address,
                                 hometown=hometown, phone=phone, num_id=id)
            return redirect("users:member")
