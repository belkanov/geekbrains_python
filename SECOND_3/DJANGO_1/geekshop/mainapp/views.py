from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from basketapp.models import Basket
from .models import Product, ProductCategory


# Create your views here.
def category(request, pk=0):
    title = "каталог"

    basket_str = ''
    if request.user.is_authenticated:
        basket_str = Basket.get_short_view_str(user=request.user)

    links_menu = ProductCategory.objects.all()
    products = Product.objects.all()
    if pk:
        if ProductCategory.objects.filter(pk=pk).exists():
            products = products.filter(category_id=pk)
        else:
            pk = 0
    else:
        # чтоб не вываливать все продукты разом (вдруг их 1к+), если перейдем на категорию "все".
        # сюда можно еще какойнить рандом добавить или других плюх, разнообразия ради
        products = products[:3]

    context = {
        'title': title,
        'links_menu': links_menu,
        'menu_links': [
            {'href': reverse('main'), 'name': 'домой'},
            {'href': reverse('categories:category'), 'name': 'продукты'},
            {'href': reverse('contacts'), 'name': 'контакты'},
        ],
        # 'categories': categories,
        'products': products,
        'basket_str': basket_str,
    }
    return render(request, 'mainapp/category.html', context)


def product(request, pk=0):
    title = "товар"

    basket_str = ''
    if request.user.is_authenticated:
        basket_str = Basket.get_short_view_str(user=request.user)

    links_menu = ProductCategory.objects.all()
    product = get_object_or_404(Product, pk=pk)

    context = {
        'title': title,
        'links_menu': links_menu,
        'menu_links': [
            {'href': reverse('main'), 'name': 'домой'},
            {'href': reverse('categories:category'), 'name': 'продукты'},
            {'href': reverse('contacts'), 'name': 'контакты'},
        ],
        # 'categories': categories,
        'product': product,
        'basket_str': basket_str,
    }
    return render(request, 'mainapp/product.html', context)