from pathlib import Path

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser


def validate_age(value):
    if value and value < 18:
        raise ValidationError('Сайт только для взрослых ;)')


# -- КАК СДЕЛАТЬ ПЕРЕЕЗД НА СВОЮ МОДЕЛЬ ПОЛЬЗОВАТЕЛЯ (это больше для себя инфа, будет куда посмотреть и не искать)
#
# -- по хорошему проект надо начинать со своих юзеров,
# -- чтобы с первой миграцией все было ОК
# -- но мы можем попасть на уже существующий проект, где этого не делали
#
# -- создаем пустую модель на основе AbstractUser, в ней обязательно
# --    class Meta:
# --     db_table = 'auth_user'
#
# -- делаем настройки в settings.py (+приложение, AUTH_USER_MODEL)
#
# -- по идее должен сработать
# -- python manage.py migrate authapp --fake-initial
# -- но из-за проверок даже для фейков будет фиаско
# -- поэтому руками делаем (SQLite синтаксис)
#
# INSERT INTO django_migrations
#        (app, name, applied)
# VALUES ('authapp', '0001_initial', CURRENT_TIMESTAMP);
#
# UPDATE django_content_type
#    SET app_label = 'authapp'
#  WHERE app_label = 'auth'
#    AND model = 'user';
#
# -- ребут сервера, тест
#
# -- если все ок:
#
# -- убираем из модели
# -- db_table = 'auth_user'
# -- это чтобы произошло переименование таблицы
# -- при необходимости добавлям свои поля
#
# -- делаем миграцию
#
# python manage.py makemigrations
# python manage.py migrate
#
# -- https://www.caktusgroup.com/blog/2019/04/26/how-switch-custom-django-user-model-mid-project/

class ShopUser(AbstractUser):
    age = models.PositiveIntegerField(
        verbose_name='возраст',
        null=True,
        validators=[validate_age]
    )
    avatar = models.ImageField(
        upload_to='users_avatars',
        blank=True
    )

    def get_avatar(self):
        if self.avatar:
            return Path(settings.MEDIA_URL / self.avatar)
        else:
            # return 'default-avatar'
            return ''


