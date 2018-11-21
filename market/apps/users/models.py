from django.db import models

# Create your models here.
from db.base_model import BaseModel


class Users(BaseModel):
    username = models.CharField(max_length=11, verbose_name="用户名")
    password = models.CharField(max_length=32, verbose_name="密码")

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.username


class Infor(BaseModel):
    sex_choices = (
        (1, "男"),
        (2, "女"),
    )
    head = models.ImageField(upload_to="static/media/", default="images/infortx.png", verbose_name="头像")
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

    def __str__(self):
        return self.nickname
