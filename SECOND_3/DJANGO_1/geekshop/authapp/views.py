from django.conf import settings
from django.contrib import auth
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserChangeForm
from authapp.models import ShopUser


# Create your views here.
def login(request):
    title = 'вход'

    login_form = ShopUserLoginForm(data=request.POST)
    if request.method == 'POST' and login_form.is_valid():  # is_valid() проверяет их корректность в соответствии с атрибутами модели.
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)  # пропишет пользователя в объект запроса request
            return HttpResponseRedirect(reverse('main'))

    context = {'title': title, 'login_form': login_form}
    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


def edit(request):
    title = 'редактирование'

    if request.method == 'POST':
        edit_form = ShopUserChangeForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('authapp:edit'))
    else:
        edit_form = ShopUserChangeForm(instance=request.user)

    context = {'title': title, 'edit_form': edit_form}
    return render(request, 'authapp/edit.html', context)


def register(request):
    title = 'регистрация'

    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            user = register_form.save()
            if send_verify_email(user):
                print(f'сообщение для {user.username} успешно отправлено')
                return HttpResponseRedirect(reverse('authapp:login'))
            else:
                print(f'сообщение для {user.username} НЕ отправлено')
                return HttpResponseRedirect(reverse('authapp:login'))
    else:
        register_form = ShopUserRegisterForm()

    context = {'title': title, 'register_form': register_form}

    return render(request, 'authapp/register.html', context)


def send_verify_email(user: ShopUser):
    verify_link = reverse('auth:verify', args=(user.activation_key,))
    title = f'Подтверждение учетной записи'
    msg = f'Здравствуйте.\n' \
          f'\nНа портале {settings.DOMAIN_NAME} была попытка зарегистрировать учетную запись на данный почтовый ящик.' \
          f'\nДля подтверждения регситрации, пожалуйста, пройдите по ссылке: ' \
          f'\n{verify_link}' \
          f'\nЕсли это были не Вы - просто проигнорируйте письмо.'

    return send_mail(title, msg, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, activation_key):
    try:
        user = ShopUser.objects.get(activation_key=activation_key)
        if not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user)
            return render(request, 'authapp/verify.html')
        else:
            print(f'не получилось активировать пользователя с кодом: {activation_key}')
            return render(request, 'authapp/verify.html')
    except ShopUser.DoesNotExist as e:
        print(f'не получилось активировать пользователя с кодом: {activation_key}\n{e.args}')
        return redirect('main')
