from django.conf import settings
from django.db import models

from authapp.models import ShopUser
from mainapp.models import Product


class Order(models.Model):
    class OrderStatusChoices(models.TextChoices):
        FORMING = 'FM', 'формируется'
        SENT_TO_PROCEED = 'STP', 'отправлен в обработку'
        PROCEEDED = 'PRD', 'оплачен'
        PAID = 'PD', 'обрабатывается'
        READY = 'RDY', 'готов к выдаче'
        CANCEL = 'CNC', 'отменен'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='создан'
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='обновлен'
    )
    status = models.CharField(
        max_length=3,
        choices=OrderStatusChoices.choices,
        default=OrderStatusChoices.FORMING,
        verbose_name='статус'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='активен'
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'Заказ {self.id}'

    def get_total_quantity(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity, items)))

    def get_product_type_quantity(self):
        return self.orderitems.select_related().count()

    def get_total_cost(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.get_product_cost(), items)))

    def delete(self):
        for item in self.orderitems.select_related():
            item.product.quantity += item.quantity
            item.product.save()

        self.is_active = False
        self.save()


class OrderItems(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='orderitems',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        verbose_name='продукт',
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(
        default=0,
        verbose_name='количество'
    )

    def get_product_cost(self):
        return self.product.price * self.quantity
