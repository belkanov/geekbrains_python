from .models import Basket


def basket(request):
    basket_str = ''
    if request.user.is_authenticated:
        basket_str = Basket.get_short_view_str(user=request.user)

    return {
        'basket_str': basket_str,
    }
