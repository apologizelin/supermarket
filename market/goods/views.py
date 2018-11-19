from django.shortcuts import render

# Create your views here.
from goods.models import Goods, Comment


def index(request):
    data = Goods.objects.all()
    context = {
        "goods": data
    }
    return render(request, "users/index.html", context)


def detail(request):
    try:
        id = request.GET.get("id")
        data = Goods.objects.get(id=id)
    except Goods.DoesNotExist:
        id = 1
        data = Goods.objects.get(id=id)
    except ValueError:
        id = 1
        data = Goods.objects.get(id=id)
    # 在数据库中查询id对应的商品
    comment = Comment.objects.filter(parent_id=id)
    context = {
        "goods": data,
        "comment": comment
    }
    return render(request, "goods/detail.html", context)
