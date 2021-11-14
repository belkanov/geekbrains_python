from django.db import models
from django.conf import settings
from django.db.models import Sum, F

from mainapp.models import Product


# Create your models here.

class Basket(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='basket'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(
        verbose_name='количество',
        default=0
    )
    add_datetime = models.DateTimeField(
        verbose_name='время добавления товара',
        auto_now_add=True
    )

    @staticmethod
    def get_short_view_str(user=None):
        if user:
            objs = Basket.objects.filter(user=user)
            _sum, _count = 0, 0
            for obj in objs:
                _count += obj.quantity
                _sum += obj.quantity * obj.product.price
            return f'{_count} шт. | {_sum} ₽'
        return None

    @property
    def price(self):
        return self.product.price * self.quantity

    @property
    def basket_count(self):
        return Basket.objects.filter(user=self.user).aggregate(Sum('quantity')).get('quantity__sum', 0)

    @property
    def basket_price(self):
        return Basket.objects.filter(user=self.user).aggregate(basket_price=Sum(F('quantity') * F('product__price')))['basket_price']
