from django import forms
from django.core.validators import RegexValidator
from django_redis import get_redis_connection

from apps.users.helper import set_password
from apps.users.models import Users


class RegForm(forms.Form):
    username = forms.CharField(error_messages={"required": "用户名不能为空"},
                               validators=[
                                   RegexValidator(r'^1[35789]\d{9}$', "手机号码格式错误")
                               ])
    password = forms.CharField(max_length=11,
                               min_length=6,
                               error_messages={"required": "密码不能为空",
                                               "max_length": "密码长度必须小于11个字节",
                                               "min_length": "用户名长度必须大于6个字节"
                                               }
                               )

    rpassword = forms.CharField(max_length=11,
                                min_length=6,
                                error_messages={"required": "密码不能为空",
                                                "max_length": "密码长度必须小于11个字节",
                                                "min_length": "用户名长度必须大于6个字节"
                                                }
                                )

    def clean(self):
        # 得到数据
        datas = self.cleaned_data
        # data = super().clean()
        if datas.get('password') != datas.get('rpassword'):
            # 验证失败
            raise forms.ValidationError({"rpassword": "两次密码不一致"})
        # 验证成功 返回所有清洗后的数据
        return datas

    def clean_username(self):
        # 验证用户名是否唯一
        username = self.cleaned_data.get('username')
        rs = Users.objects.filter(username=username).exists()  # 返回bool
        if rs:
            raise forms.ValidationError("手机号码已经被注册")
        return username


# 短信验证
verify_code = forms.CharField(error_messages={"required": "请填写验证"})


# 单独使用一个方法校验 验证码
def clean_verify_code(self):
    # 验证验证码是否填写正确
    # 获取redis中的验证码
    r = get_redis_connection()
    tel = self.cleaned_data.get('phone')
    s_code = r.get(tel)
    if not s_code:
        raise forms.ValidationError("验证码已经过期")
    # 表单传入的验证码
    verify_code = self.cleaned_data.get('verify_code')
    # sid_verify_code = self.data.get('sid_verify_code')
    if str(verify_code) != str(s_code):
        raise forms.ValidationError("验证码输入有误")
    return verify_code


class LoadForm(forms.Form):
    username = forms.CharField(max_length=11,
                               min_length=11,
                               error_messages={"required": "请输入用户名",
                                               "max_length": "格式不正确,请确认用户名",
                                               "min_length": "格式不正确,请确认用户名"
                                               }
                               )
    password = forms.CharField(max_length=11,
                               min_length=6,
                               error_messages={"required": "请输入密码",
                                               "max_length": "格式不正确,请确认密码",
                                               "min_length": "格式不正确,请确认密码"
                                               })

    # widgets = {  # 样式
    #     'username': forms.TextInput(attrs={"class": "login-name", "placeholder": '请输入手机号'}),
    #     'password': forms.PasswordInput(attrs={"class": "login-password", "placeholder": '请输入密码'}),
    # }

    def clean(self):  # 综合校验
        cleaned_data = self.cleaned_data
        # 获取用手机和密码
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        # 验证手机号码是否存在
        if all([username, password]):
            # 获取用户
            try:
                user = Users.objects.get(username=username)
            except Users.DoesNotExist:
                raise forms.ValidationError({"username": "该用户不存在!"})

            # 判断密码是否正确
            if user.password != set_password(password):
                raise forms.ValidationError({"password": "密码填写错误!"})

            # 正确
            # 将用户信息保存到cleaned_data中
            cleaned_data['user'] = user
            return cleaned_data
        else:
            return cleaned_data
