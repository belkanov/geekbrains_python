from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import ShopUser

# Register your models here.
admin.site.register(ShopUser, UserAdmin)
