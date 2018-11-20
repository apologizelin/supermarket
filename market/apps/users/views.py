import hashlib
from django.shortcuts import render, redirect
from django.views import View

from apps.users.forms import RegForm, LoadForm
from apps.users.helper import set_password, login
from apps.users.models import Users, Infor


# 注册
# def register(request):
#     if request.method == "GET":
#         # 显示注册页面
#         return render(request, "users/reg.html")
#     else:
#         datas = request.POST
#         form = RegForm(datas)
#         # 表单验证
#         if form.is_valid():
#             datas = form.cleaned_data
#             # 注册并保存到数据库
#             username = datas.get("username")
#             pwd = datas.get("password")
#             ha = hashlib.md5(pwd.encode("utf-8"))
#             pwd = ha.hexdigest()
#             user = Users.objects.filter(username=username)
#             if user:
#                 return render(request, "users/reg.html")
#             else:
#                 Users.objects.create(username=username, password=pwd)
#                 return redirect("users:登陆")
#         else:
#             context = {
#                 "errors": form.errors,
#                 "datas": datas
#             }
#             return render(request, "users/reg.html", context)


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


# 登陆
# def load(request):
#     if request.method == "GET":
#         return render(request, "users/login.html")
#     else:
#         data = request.POST
#         form = LoadForm(data)
#         # 表单验证
#         if form.is_valid():
#             data = form.cleaned_data
#             username = data.get("username")
#             pwd = data.get("password")
#             try:
#                 user = Users.objects.get(username=username)
#             except Users.MultipleObjectsReturned:
#                 # 获取多个记录
#                 return redirect("users:登陆")
#             except Users.DoesNotExist:
#                 return redirect("users:登陆")
#             ha = hashlib.md5(pwd.encode("utf-8"))
#             pwd = ha.hexdigest()
#             # 验证账户
#             if pwd == user.password:
#                 request.session["ID"] = user.id
#                 request.session["username"] = user.username
#                 return redirect("users:个人中心")
#             else:
#                 return redirect("users:登陆")
#         else:
#             context = {
#                 "errors": form.errors,
#                 "data": data
#             }
#             return render(request, "users/login.html", context)


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
            # 跳转到用户中心页面
            return redirect('users:member')
        else:
            context = {
                "errors": form.errors
            }
            return render(request, "users/login.html", context)
        # if form.is_valid():
        #     data = form.cleaned_data
        #     username = data.get("username")
        #     pwd = data.get("password")
        #     try:
        #         user = Users.objects.get(username=username)
        #     except Users.MultipleObjectsReturned:
        #         # 获取多个记录
        #         return redirect("users:login")
        #     except Users.DoesNotExist:
        #         return redirect("users:login")
        #     pwd = set_password(pwd)
        #     # 验证账户
        #     if pwd == user.password:
        #         request.session["ID"] = user.id
        #         request.session["username"] = user.username
        #         return redirect("users:member")
        #     else:
        #         return redirect("users:login")
        # else:
        #     context = {
        #         "errors": form.errors,
        #         "data": data
        #     }
        #     return render(request, "users/login.html", context)


class ForgetPassView(View):
    def get(self, request):
        return render(request, "users/forgetpassword.html")

    def post(self, request):
        return render(request, "users/forgetpassword.html")


# 个人中心
# def member(request):
#     # 获取session中的用户名
#     username = request.session.get("username")
#     # 判断用户名是否存在,不存在则跳转登陆界面,否则跳转个人中心
#     if username:
#         context = {
#             "username": username
#         }
#         return render(request, "users/member.html", context)
#     else:
#         return redirect("users:登陆")


class MemberView(View):
    """个人中心"""

    def get(self, request):
        username = request.session.get("username")
        context = {
            "username": username
        }
        return render(request, "users/member.html", context)


# 个人资料
# def infor(request):
#     if request.method == "GET":
#         id = request.session.get("ID")
#         # 捕获异常,有数据就回显,没有数据则显示添加数据的提示信息
#         try:
#             info = Infor.objects.get(num_id=id)
#         except:
#             return render(request, "users/infor.html")
#         context = {
#             "info": info
#         }
#         return render(request, "users/infor.html", context)
#     else:
#         # 获取post中表单提交的数据
#         data = request.POST
#         nickname = data.get("nickname")
#         sex = data.get("sex")
#         birthday = data.get("birthday")
#         school = data.get("school")
#         address = data.get("address")
#         hometown = data.get("hometown")
#         phone = data.get("phone")
#         id = request.session.get("ID")
#         info = Infor.objects.filter(num_id=id)
#         context = {
#             "info": data
#         }
#         # 判断是否填写过个人资料,填写过再提交便做更新,否则创建
#         if info:
#             Infor.objects.filter(num_id=id).update(nickname=nickname, sex=sex, birthday=birthday, school=school,
#                                                    address=address, hometown=hometown, phone=phone, num_id=id)
#             return render(request, "users/infor.html", context)
#         else:
#             Infor.objects.create(nickname=nickname, sex=sex, birthday=birthday, school=school, address=address,
#                                  hometown=hometown, phone=phone, num_id=id)
#             return render(request, "users/infor.html", context)


class InfomationView(View):
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
        info = Infor.objects.filter(num_id=id)
        # 判断是否填写过个人资料,填写过再提交便做更新,否则创建
        if info:
            Infor.objects.filter(num_id=id).update(nickname=nickname, sex=sex, birthday=birthday, school=school,
                                                   address=address, hometown=hometown, phone=phone, num_id=id)
            return redirect("users:member")
        else:
            Infor.objects.create(nickname=nickname, sex=sex, birthday=birthday, school=school, address=address,
                                 hometown=hometown, phone=phone, num_id=id)
            return redirect("users:member")
