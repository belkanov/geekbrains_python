from django.urls import path

import ordersapp.views
app_name = 'ordersapp'

urlpatterns = [
    path('', ordersapp.views.OrderList.as_view(), name='orders_list'),
    path('forming/complete/<int:pk>/', ordersapp.views.order_forming_complete, name='order_forming_complete'),
    path('create/', ordersapp.views.OrderItemsCreate.as_view(), name='order_create'),
    path('read/<int:pk>/', ordersapp.views.OrderRead.as_view(), name='order_read'),
    path('update/<int:pk>/', ordersapp.views.OrderItemsUpdate.as_view(), name='order_update'),
    path('delete/<int:pk>/', ordersapp.views.OrderDelete.as_view(), name='order_delete'),
]
