from django.urls import path
import adminapp.views as adminapp

app_name = 'adminnapp'

urlpatterns = [
    path('dflt/', adminapp.dflt, name='dflt'),

    path('user/create', adminapp.user_create, name='user_create'),
    path('user/read', adminapp.user_read, name='user_read'),
    path('user/update/<int:pk>', adminapp.user_update, name='user_update'),
    path('user/delete/<int:pk>', adminapp.user_delete, name='user_delete'),

    # path('category/create', adminapp.category_create, name='category_create'),
    path('category/create', adminapp.CategoryCreateView.as_view(), name='category_create'),
    # path('category/read', adminapp.category_read, name='category_read'),
    path('category/read', adminapp.CategoryListView.as_view(), name='category_read'),
    # path('category/update/<int:pk>', adminapp.category_update, name='category_update'),
    path('category/update/<int:pk>', adminapp.CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>', adminapp.category_delete, name='category_delete'),

    path('product/create', adminapp.product_create, name='product_create'),
    path('product/read', adminapp.product_read, name='product_read'),
    path('product/read/category/<int:pk>/page/<int:page>', adminapp.products_read, name='products_read'),
    path('product/update/<int:pk>', adminapp.product_update, name='product_update'),
    path('product/delete/<int:pk>', adminapp.product_delete, name='product_delete'),
]
