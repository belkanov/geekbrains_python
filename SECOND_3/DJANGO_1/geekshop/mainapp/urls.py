from django.urls import path
from .views import category, product

app_name = 'mainapp'
urlpatterns = [
    path('<int:pk>', category, name='category'),
    path('', category, name='category'),
    path('product/<int:pk>', product, name='product'),
]
