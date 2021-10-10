from django.shortcuts import render
from django.conf import settings


def main(request):
    # print(settings.STATICFILES_DIRS)
    return render(request, 'geekshop/index.html')


def contacts(request):
    return render(request, 'geekshop/contact.html')
