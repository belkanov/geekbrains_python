from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView

from adminapp.forms import ShopUserAdminChangeForm, ProductCategoryAdminChangeForm, ProductCategoryAdminCreateForm, ProductAdminChangeForm, ProductAdminCreateForm
from authapp.forms import ShopUserChangeForm, ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import Product, ProductCategory


# Create your views here.

def dflt(request):
    # context = {}
    # return render(request, 'adminapp/base.html', context)
    pass


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    title = 'пользователи/создание'

    if request.method == 'POST':
        create_form = ShopUserRegisterForm(request.POST, request.FILES)
        if create_form.is_valid():
            create_form.save()
            return redirect('adminka:user_read')
    else:
        create_form = ShopUserRegisterForm()

    context = {
        'title': title,
        'create_form': create_form
    }

    return render(request, 'adminapp/user_create.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_read(request):
    title = 'админка/пользователи'

    users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')

    context = {
        'title': title,
        'users_list': users_list,
    }

    return render(request, 'adminapp/users.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    title = 'пользователи/редактирование'
    edit_user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        edit_form = ShopUserAdminChangeForm(request.POST, request.FILES, instance=edit_user)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('adminka:user_update', pk=edit_user.pk)
    else:
        edit_form = ShopUserAdminChangeForm(instance=edit_user)

    context = {
        'title': title,
        'update_form': edit_form
    }

    return render(request, 'adminapp/user_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    del_user = get_object_or_404(ShopUser, pk=pk)
    # if request.method == 'POST':
    del_user.is_active = False
    del_user.save()
    return redirect('adminka:user_read')


# @user_passes_test(lambda u: u.is_superuser)
# def category_create(request):
#     title = 'категории/создание'
#
#     if request.method == 'POST':
#         create_form = ProductCategoryAdminCreateForm(request.POST)
#         if create_form.is_valid():
#             create_form.save()
#             return redirect('adminka:category_read')
#     else:
#         create_form = ProductCategoryAdminCreateForm()
#
#     context = {
#         'title': title,
#         'create_form': create_form
#     }
#
#     return render(request, 'adminapp/category_create.html', context)


class CategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_create.html'
    success_url = reverse_lazy('adminka:category_read')
    fields = '__all__'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/создание'
        return context


# @user_passes_test(lambda u: u.is_superuser)
# def category_read(request):
#     title = 'админка/категории'
#
#     categories_list = ProductCategory.objects.all().order_by('-is_active', 'name')
#
#     context = {
#         'title': title,
#         'categories_list': categories_list,
#     }
#
#     return render(request, 'adminapp/categories.html', context)


class CategoryListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'админка/категории'
        return context


# @user_passes_test(lambda u: u.is_superuser)
# def category_update(request, pk):
#     title = 'категории/редактирование'
#     edit_category = get_object_or_404(ProductCategory, pk=pk)
#
#     if request.method == 'POST':
#         edit_form = ProductCategoryAdminChangeForm(request.POST, instance=edit_category)
#         if edit_form.is_valid():
#             edit_form.save()
#             return redirect('adminka:category_update', pk=edit_category.pk)
#     else:
#         edit_form = ProductCategoryAdminChangeForm(instance=edit_category)
#
#     context = {
#         'title': title,
#         'update_form': edit_form
#     }
#
#     return render(request, 'adminapp/user_update.html', context)


class CategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('adminka:category_read')
    fields = '__all__'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/редактирование'
        return context


@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk):
    del_category = get_object_or_404(ProductCategory, pk=pk)
    # if request.method == 'POST':
    del_category.is_active = False
    del_category.save()
    return redirect('adminka:category_read')


@user_passes_test(lambda u: u.is_superuser)
def product_create(request):
    title = 'продукты/создание'

    if request.method == 'POST':
        create_form = ProductAdminCreateForm(request.POST)
        if create_form.is_valid():
            create_form.save()
            return redirect('adminka:products_read', pk=0)
    else:
        create_form = ProductAdminCreateForm()

    context = {
        'title': title,
        'create_form': create_form
    }

    return render(request, 'adminapp/product_create.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_read(request):
    pass


@user_passes_test(lambda u: u.is_superuser)
def products_read(request, pk=0, page=1):
    title = 'админка/продукты'
    category = None

    products_list = Product.objects.all()
    if pk != 0:
        category = get_object_or_404(Product, pk=pk)
        products_list = products_list.filter(category=category)
    products_list = products_list.order_by('-is_active', 'name')

    paginator = Paginator(products_list, 4)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    context = {
        'title': title,
        'category': category,
        'products_list': products_paginator,
    }
    return render(request, 'adminapp/products.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    title = 'продукты/редактирование'
    edit_product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        edit_form = ProductAdminChangeForm(request.POST, instance=edit_product)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('adminka:product_update', pk=edit_product.pk)
    else:
        edit_form = ProductAdminChangeForm(instance=edit_product)

    context = {
        'title': title,
        'update_form': edit_form
    }

    return render(request, 'adminapp/user_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    del_product = get_object_or_404(Product, pk=pk)
    del_product.is_active = False
    del_product.save()
    return redirect('adminka:products_read', pk=0)
