from django.core.management.base import BaseCommand

from authapp.models import ShopUser, ShopUserProfile


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = ShopUser.objects.all()
        for usr in users:
            user_profile = ShopUserProfile.objects.create(user=usr)
            user_profile.save()
