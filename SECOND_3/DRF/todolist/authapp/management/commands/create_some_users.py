from django.core.management.base import BaseCommand

from authapp.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('Creating users... ', end='')
        super_user = User.objects.create_superuser('admin', 'admin@geekshop.ru', '123', first_name='admin_fn', last_name='admin_ln')
        user_1 = User.objects.create_user(username='user_1', password='111', email='user_1@geekshop.ru', first_name='Петя', last_name='Васечкин')
        user_2 = User.objects.create_user(username='user_2', password='222', email='user_2@geekshop.ru', first_name='Вася', last_name='Пупкин')
        print('DONE')
