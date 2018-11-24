from django.db import models
from db.base_model import BaseModel


# 轮播表
class LunBo(BaseModel):
    name = models.CharField(max_length=100, verbose_name="轮播名称")
    goods_sku = models.ForeignKey(to="Goodsku", verbose_name="商品sku")
    pic_url = models.ImageField(upload_to="goods/banner", verbose_name="图片地址")
    order = models.IntegerField(verbose_name="排序")

    class Meta:
        db_table = "lunbo"
        verbose_name = "轮播表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 首页活动表
class Active(BaseModel):
    name = models.CharField(max_length=100, verbose_name="名称")
    pic = models.ImageField(upload_to="goods/%Y%m", default="images/s1.png", verbose_name="图片")
    url = models.CharField(max_length=200, default="", verbose_name="url地址")

    class Meta:
        db_table = "active"
        verbose_name = "首页活动表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 特色专区表
class AreaGoods(BaseModel):
    name = models.CharField(max_length=100, verbose_name="名称")
    script = models.CharField(max_length=200, verbose_name="描述")
    order = models.IntegerField(verbose_name="排序")

    class Meta:
        db_table = "areaGoods"
        verbose_name = "特色专区表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 专区商品表
class Produce(BaseModel):
    area_id = models.ForeignKey(to="AreaGoods", verbose_name="特色专区id")
    goods_id = models.ForeignKey(to="Goodsku", verbose_name="商品sku表id")

    class Meta:
        db_table = "produce"
        verbose_name = "专区商品表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.area_id


# 商品分类表
class Assortment(BaseModel):
    name = models.CharField(max_length=100, verbose_name="分类名")
    introduce = models.CharField(max_length=200, verbose_name="分类简介")

    class Meta:
        db_table = "assortment"
        verbose_name = "商品分类表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 商品spu表
class Good(BaseModel):
    name = models.CharField(max_length=100, verbose_name="商品名称")
    detail = models.CharField(max_length=200, verbose_name="商品详情")

    class Meta:
        db_table = "good"
        verbose_name = "商品spu表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 商品sku表
class Goodsku(BaseModel):
    unit_choices = (
        (1, "件"),
        (2, "斤"),
        (3, "箱"),
    )
    name = models.CharField(max_length=100, verbose_name="商品名称")
    introduce = models.CharField(max_length=200, default="", verbose_name="商品简介")
    unit = models.IntegerField(choices=unit_choices, default=1, verbose_name="单位")
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="商品价格")
    stock = models.IntegerField(default=0, verbose_name="库存")
    sale_num = models.IntegerField(default=0, verbose_name="销量")
    logo_url = models.ImageField(upload_to="goods/%Y%m", default="", verbose_name="logo地址")
    isGround = models.BooleanField(default=True, verbose_name="是否上架")
    assortment_id = models.ForeignKey(to="Assortment", default=0, verbose_name="商品分类id")
    good_id = models.ForeignKey(to="Good", default=0, verbose_name="商品spu表id")

    class Meta:
        db_table = "goods"
        verbose_name = "商品sku表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 商品相册表
class GoodPic(BaseModel):
    pic_url = models.ImageField(upload_to="goods/pic", verbose_name="图片地址")
    good_id = models.ForeignKey(to="Goodsku", verbose_name="商品id")

    class Meta:
        db_table = "goods_pic"
        verbose_name = "商品相册表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.good_id


# 评论表
class Comment(BaseModel):
    name = models.CharField(max_length=30, default="", verbose_name="买家名")
    content = models.CharField(max_length=200, default="", null=True, verbose_name="评论内容")
    parent = models.ForeignKey(to="Goodsku", verbose_name="商品skuid")

    class Meta:
        db_table = "comment"
        verbose_name = "评论表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content
