from django.shortcuts import render

# Create your views here.
from apps.goods.models import Goodsku, Comment, Active, Assortment, LunBo


def index(request):
    active = Active.objects.all()
    lunbo = LunBo.objects.all()
    goods = Goodsku.objects.all()
    context = {
        "active": active,
        "lunbo": lunbo,
        "goods": goods,
    }
    return render(request, "users/index.html", context)


def detail(request):
    try:
        id = request.GET.get("id")
        data = Goodsku.objects.get(id=id)
    except Goodsku.DoesNotExist:
        id = 1
        data = Goodsku.objects.get(id=id)
    except ValueError:
        id = 1
        data = Goodsku.objects.get(id=id)
    # 在数据库中查询id对应的商品
    comment = Comment.objects.filter(parent_id=id)
    context = {
        "goods": data,
        "comment": comment
    }
    return render(request, "goods/detail.html", context)


def category(request):
    id = request.GET.get("c_id")
    print(id)
    assort = Assortment.objects.all()
    goods = Goodsku.objects.filter(assortment_id=id)
    print(goods)
    context = {
        "assort": assort,
        "goods": goods,
    }
    return render(request, "goods/category.html", context)
