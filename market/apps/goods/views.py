from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from apps.goods.models import Goodsku, Comment, Active, Assortment, LunBo, AreaGoods


def index(request):
    active = Active.objects.all()
    lunbo = LunBo.objects.all()
    areas = AreaGoods.objects.all()
    context = {
        "active": active,
        "lunbo": lunbo,
        "areas": areas,
    }
    return render(request, "users/index.html", context)


def detail(request, id):
    try:
        data = Goodsku.objects.get(id=id)
    except Goodsku.DoesNotExist:
        return redirect("goods:首页")
    except ValueError:
        return redirect("goods:首页")
    # 在数据库中查询id对应的商品
    comment = Comment.objects.filter(parent_id=id)
    context = {
        "goods": data,
        "comment": comment
    }
    return render(request, "goods/detail.html", context)


def category(request, c_id, order):
    """
    排序规则:综合(0),销量(1),价格降(2),价格升(3),新品(4)
    """
    c_id = int(c_id)
    order = int(order)
    # 获取分类
    assort = Assortment.objects.filter(isDelete=False).order_by("-order")
    # 查询分类下的商品 默认查询第一个分类
    if c_id == 0:
        ass = assort.first()
        c_id = ass.pk
    goods = Goodsku.objects.filter(isDelete=False, isGround=True, assortment_id=c_id)
    or_list = ["id", "-sale_num", "-price", "price", "time"]
    try:
        one = or_list[order]
    except:
        one = or_list[0]
        order = 0
    goods = goods.order_by(one)

    # 分页
    pageSize = 10  # 每页显示条数
    paginator = Paginator(goods, pageSize)  # 获取分页对象
    # 获取分页数据
    p = request.GET.get('p', 1)  # 获取当前页,默认1
    try:
        page = paginator.page(p)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        page = paginator.page(1)

    # 渲染页面
    context = {
        "assort": assort,
        "goods": page,
        "c_id": c_id,
        "order": order,
    }
    return render(request, "goods/category.html", context)
