from django.urls import path
from .views import category

app_name = 'mainapp'
urlpatterns = [
    path('<int:pk>', category, name='category'),
    path('', category, name='category'),
]
