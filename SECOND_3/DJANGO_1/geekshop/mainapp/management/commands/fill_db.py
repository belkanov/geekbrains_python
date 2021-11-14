import json
from pathlib import Path

from django.core.management.base import BaseCommand

from authapp.models import ShopUser
from mainapp.models import Product, ProductCategory

JSON_PATH = Path('mainapp/json')


def load_from_json(file_name):
    with (JSON_PATH / file_name).open(mode='r', encoding='utf8') as f:
        return json.load(f)


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = load_from_json('categories.json')
        ProductCategory.objects.all().delete()
        for category in categories:
            new_category = ProductCategory(**category)
            new_category.save()

        products = load_from_json('products.json')
        Product.objects.all().delete()
        for product in products:
            _category = ProductCategory.objects.get(id=product['category'])
            product['category'] = _category
            new_product = Product(**product)
            new_product.save()

        super_user = ShopUser.objects.create_superuser('django_admin', 'admin@geekshop.ru', 'superpass123', age=120)
