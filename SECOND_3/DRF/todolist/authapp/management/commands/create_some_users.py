from django.core.management.base import BaseCommand

from authapp.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('Creating users ...', end='')
        super_user = User.objects.create_superuser('admin', 'admin@geekshop.ru', '123')
        user_1 = User.objects.create_user(username='user_1', password='111', email='user_1@geekshop.ru')
        user_2 = User.objects.create_user(username='user_2', password='222', email='user_2@geekshop.ru')
        print('DONE')
