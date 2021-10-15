from django.shortcuts import render
from .models import Product, ProductCategory


# Create your views here.
def products(requset, pk=None):
    product_categories = ProductCategory.objects.all()
    products_data = Product.objects.all()
    if pk:
        products_data = products_data.filter(category_id=pk)
    else:
        # чтоб не вываливать все продукты разом (вдруг их 1к+), если перейдем на категорию "все".
        # сюда можно еще какойнить рандом добавить или других плюх, разнообразия ради
        products_data = products_data[:3]

    context = {
        'title': 'каталог',
        'menu_links': [
            {'href': 'main', 'name': 'домой'},
            {'href': 'products:index', 'name': 'продукты'},
            {'href': 'contacts', 'name': 'контакты'},
        ],
        'product_categories': product_categories,
        'products_data': products_data,
    }
    return render(requset, 'mainapp/products.html', context)
