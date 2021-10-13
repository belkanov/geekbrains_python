from django.shortcuts import render


# Create your views here.
def products(requset):
    context = {
        'title': 'каталог',
        'menu_links': [
            {'href': 'main', 'name': 'домой'},
            {'href': 'products', 'name': 'продукты'},
            {'href': 'contacts', 'name': 'контакты'},
        ]
    }
    return render(requset, 'mainapp/products.html', context)
