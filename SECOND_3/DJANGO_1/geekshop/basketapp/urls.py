from django.urls import path
import basketapp.views as basketapp

app_name = 'basketapp'

urlpatterns = [
    path('', basketapp.basket, name='view'),
    path('data/', basketapp.basket_data, name='data'),
    path('edit/<int:pk>/<int:value>', basketapp.basket_edit, name='edit'),
    path('add/<int:pk>', basketapp.basket_add, name='add'),
]
