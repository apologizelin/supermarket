from django.db import models


# Create your models here.
class Goods(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    time = models.DateField(auto_now=True)
    url = models.CharField(max_length=100, default="")

    class Meta:
        db_table = "goods"

    def __str__(self):
        return self.name


class Comment(models.Model):
    name = models.CharField(max_length=30, default="")
    content = models.CharField(max_length=200, default="", null=True)
    time = models.DateField(auto_now_add=True)
    parent = models.ForeignKey(to="Goods")

    class Meta:
        db_table = "comment"

    def __str__(self):
        return self.content
