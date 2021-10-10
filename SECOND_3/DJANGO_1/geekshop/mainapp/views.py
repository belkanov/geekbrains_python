from django.shortcuts import render


# Create your views here.
def products(requset):
    return render(requset, 'mainapp/products.html')
