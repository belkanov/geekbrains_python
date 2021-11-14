from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from basketapp.models import Basket
from .models import Product, ProductCategory


# Create your views here.
def category(request, pk=0, page=1):
    title = "каталог"

    links_menu = ProductCategory.objects.all()
    products = Product.objects.all()
    if pk:
        if ProductCategory.objects.filter(pk=pk).exists():
            products = products.filter(category_id=pk)
        else:
            pk = 0

    paginator = Paginator(products, 2)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    context = {
        'title': title,
        'links_menu': links_menu,
        'menu_links': [
            {'href': reverse('main'), 'name': 'домой'},
            {'href': reverse('categories:category', kwargs={'pk': 0, 'page': 1}), 'name': 'продукты'},
            {'href': reverse('contacts'), 'name': 'контакты'},
        ],
        # 'categories': categories,
        'products': products_paginator,
    }
    return render(request, 'mainapp/category.html', context)


def product(request, pk=0):
    title = "товар"

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
    }
    return render(request, 'mainapp/product.html', context)