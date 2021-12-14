from django.urls import path
from .views import category, product
from django.views.decorators.cache import cache_page

app_name = 'mainapp'
urlpatterns = [
    path('<int:pk>/page/<int:page>', cache_page(3600)(category), name='category'),
    path('', cache_page(3600)(category), name='category'),
    path('product/<int:pk>', product, name='product'),
]
