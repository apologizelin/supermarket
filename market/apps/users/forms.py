from django import forms
from django.core.validators import RegexValidator


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
