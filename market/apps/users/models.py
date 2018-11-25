from django.db import models

from db.base_model import BaseModel


class Users(BaseModel):
    """用户账号表"""
    username = models.CharField(max_length=11, verbose_name="用户名")
    password = models.CharField(max_length=32, verbose_name="密码")

    class Meta:
        db_table = "users"
        verbose_name = "账号表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class Infor(BaseModel):
    """用户个人资料表"""
    sex_choices = (
        (1, "男"),
        (2, "女"),
    )
    head = models.ImageField(upload_to="users", default="images/infortx.png", verbose_name="头像")
    nickname = models.CharField(max_length=20, verbose_name="昵称", null=True, blank=True)
    sex = models.SmallIntegerField(choices=sex_choices, verbose_name="性别", default=1)
    birthday = models.DateField(verbose_name="生日", null=True, blank=True)
    school = models.CharField(max_length=100, verbose_name="学校", null=True, blank=True)
    address = models.CharField(max_length=100, verbose_name="地址", null=True, blank=True)
    hometown = models.CharField(max_length=100, verbose_name="故乡", null=True, blank=True)
    phone = models.CharField(max_length=11, verbose_name="手机号码", null=True, blank=True)
    num = models.OneToOneField(to="Users")

    class Meta:
        db_table = "infor"
        verbose_name = "个人资料表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.nickname


class UserAddress(BaseModel):
    """用户收货地址管理"""
    user = models.ForeignKey(to="Users", verbose_name="用户名")
    username = models.CharField(max_length=100, verbose_name="收货人")
    phone = models.CharField(max_length=11, verbose_name="收货人电话")
    proper = models.CharField(max_length=100, blank=True, default='', verbose_name="省")
    city = models.CharField(max_length=100, verbose_name="市")
    area = models.CharField(max_length=100, blank=True, default='', verbose_name="区")
    brief = models.CharField(max_length=255, verbose_name="详细地址")
    isDefault = models.BooleanField(default=False, blank=True, verbose_name="是否设置为默认")

    class Meta:
        db_table = "useraddress"
        verbose_name = "收货地址表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
