import json
from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.db.transaction import atomic

from basketapp.models import Basket
from mainapp.models import Product


def main(request):
    products_list = Product.objects.all()[:3]
    basket_str = ''
    if request.user.is_authenticated:
        basket_str = Basket.get_short_view_str(user=request.user)

    context = {
        'title': 'магазин',
        'menu_links': [
            {'href': 'main', 'name': 'домой'},
            {'href': 'categories:category', 'name': 'продукты'},
            {'href': 'contacts', 'name': 'контакты'},
        ],
        'products_list': products_list,
        'basket_str': basket_str,
    }
    return render(request, 'geekshop/index.html', context)


def contacts(request):
    basket_str = ''
    if request.user.is_authenticated:
        basket_str = Basket.get_short_view_str(user=request.user)

    context = {
        'title': 'контакты',
        'menu_links': [
            {'href': 'main', 'name': 'домой'},
            {'href': 'categories:category', 'name': 'продукты'},
            {'href': 'contacts', 'name': 'контакты'},
        ],
        'contacts_data': [],
        'basket_str': basket_str,
    }

    with open(settings.BASE_DIR / 'geekshop/json/contacts_data.json', mode='r', encoding='utf-8') as f_in:
        contacts_data = json.loads(f_in.read())
        context['contacts_data'] = contacts_data

    return render(request, 'geekshop/contact.html', context)


# для тестов http://127.0.0.1:8000/load_db_data/load_db_1.json
def load_db_data(request, f_name=None):
    # это вроде как тех. работа, поэтому пишу отдельную функцию для вывода, чтобы не переделывать __str__
    def print_models(obj_list: list[Product]):
        return f'loaded {len(file_data)} new object(s)\n\n' + '\n'.join(map(lambda x: f'[{x.pk}] {x.name} ({x.category.name})', obj_list))

    file = settings.BASE_DIR / 'geekshop/json' / f_name
    if file.exists():
        with file.open(mode='r', encoding='utf-8') as f:
            # тут я считаю, что инфа в файле валидна от слова совсем, чтобы не писать 100500 проверок
            file_data = json.load(f)
            new_ids = []
            with atomic():  # если вдруг объектов много - чтоб быстрее работало
                for item in file_data:
                    new_product = Product(name=item['name'], category_id=item['category_id'])
                    new_product.save()
                    new_ids.append(new_product.pk)
            new_objs = Product.objects.filter(pk__in=new_ids)
        return HttpResponse(print_models(new_objs), content_type='application/json')  # content_type для более читабельного вида
    else:
        raise Http404()
