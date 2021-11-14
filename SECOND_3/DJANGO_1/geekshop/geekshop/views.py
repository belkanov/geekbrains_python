from django.conf import settings
from django.shortcuts import render
import json


def main(request):
    context = {
        'title': 'магазин',
        'menu_links': [
            {'href': 'main', 'name': 'домой'},
            {'href': 'products', 'name': 'продукты'},
            {'href': 'contacts', 'name': 'контакты'},
        ]
    }
    return render(request, 'geekshop/index.html', context)


def contacts(request):
    # 4. Организовать вывод динамического контента на страницах (элементы меню, список товара, заголовок страницы).
    # я вместо товара сделал контакты, они же для п.5:
    # 5. *Организовать загрузку динамического контента в контроллеры с жесткого диска (например, в формате «json»).

    context = {
        'title': 'контакты',
        'menu_links': [
            {'href': 'main', 'name': 'домой'},
            {'href': 'products', 'name': 'продукты'},
            {'href': 'contacts', 'name': 'контакты'},
        ],
        'contacts_data': [],
    }
    with open(settings.BASE_DIR / 'geekshop/json/contacts_data.json', mode='r', encoding='utf-8') as f_in:
        contacts_data = json.loads(f_in.read())
        context['contacts_data'] = contacts_data
    return render(request, 'geekshop/contact.html', context)
