from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from mainapp.models import Product
from .models import Basket


# Create your views here.

@login_required
def basket(request):
    context = {
        'title': 'корзина',
        'menu_links': [
            {'href': reverse('main'), 'name': 'домой'},
            {'href': reverse('categories:category'), 'name': 'продукты'},
            {'href': reverse('contacts'), 'name': 'контакты'},
            {'href': reverse('basket:view'), 'name': 'корзина'},
        ],
    }
    return render(request, 'basketapp/basket.html', context)


@login_required
def basket_data(request):
    if request.is_ajax():
        basket_objs = []
        if request.user.is_authenticated:
            basket_objs = Basket.objects.filter(user=request.user)
            basket_objs = [*basket_objs.values('id', 'product__name', 'product__category__name', 'quantity', 'product__price')]

        return JsonResponse({'basket_objs': list(basket_objs)})


@login_required
def basket_edit(request, pk, value):
    edit_result = False
    if request.is_ajax():
        basket_obj = get_object_or_404(Basket, pk=pk)
        if basket_obj.user == request.user:
            if value > 0:
                basket_obj.quantity = value
                basket_obj.save()
                edit_result = True
            else:
                basket_obj.delete()
                edit_result = True
    return JsonResponse({'editResultIsOK': edit_result})


@login_required
def basket_add(request, pk):
    product = get_object_or_404(Product, pk=pk)
    basket = Basket.objects.filter(user=request.user, product=product).first()
    if basket:
        basket.quantity = F('quantity') + 1
    else:
        basket = Basket(user=request.user, product=product)
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
