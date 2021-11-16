from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now

from datetime import timedelta


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
#
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# UPD: как выяснилось - метод не очень..
# как минимум в таблицах вида
# <APP>_<NewUserModel>_groups (authapp_shopuser_groups)
# <APP>_<NewUserModel>_user_permissions (authapp_shopuser_user_permissions)
# надо поле user_id поменять на
# <newusermodel>_id (shopuser_id)
# иначе при создании форм и выборе всех полей (fields = '__all__') будет ошибка из-за отсутсвующего поля в бд
# (ссылаться будет на новое, а в бд - старое)
#
# еще в django_content_type апдейт выше (SET app_label) - не нужен.
# Записей с моделью 'user' вообще не должно быть:
# auth,user -> <APP>,<newusermodel> (authapp,shopuser)
#
# возможно это все отличия, но это не точно =)
# не стал ковырять и дропнул миграции


class ShopUser(AbstractUser):
    age = models.PositiveIntegerField(
        verbose_name='возраст',
        null=True,
        blank=True,
        validators=[validate_age]
    )
    avatar = models.ImageField(
        upload_to='users_avatars',
        blank=True
    )
    activation_key = models.CharField(
        max_length=128,
        blank=True
    )

    def get_expires_time():
        return now() + timedelta(hours=24)

    activation_key_expires = models.DateTimeField(
        default=get_expires_time
    )

    def is_activation_key_expired(self):
        if now() <= self.activation_key_expires:
            return False
        return True

    def get_avatar(self):
        if self.avatar:
            # return self.avatar.url
            return f'<img src="{self.avatar.url}" class="img-circle elevation-2" alt="User Image">'
        else:
            # return 'default-avatar'
            return '<i class="fas fa-user fa-2x"></i>'

    def get_name(self):
        return self.first_name or 'пользователь'


class ShopUserProfile(models.Model):
    class SexChoices(models.TextChoices):
        MALE = 'M', 'М'
        FEMALE = 'F', 'Ж'

    user = models.OneToOneField(
        ShopUser,
        unique=True,
        null=False,
        db_index=True,
        on_delete=models.CASCADE
    )
    tagline = models.CharField(
        max_length=128,
        blank=True,
        verbose_name='тэги'
    )
    about_me = models.TextField(
        max_length=512,
        blank=True,
        verbose_name='о себе'
    )
    sex = models.CharField(
        max_length=1,
        choices=SexChoices.choices,
        blank=True,
        verbose_name='пол'
    )

    @receiver(post_save, sender=ShopUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            ShopUserProfile.objects.create(user=instance)

    @receiver(post_save, sender=ShopUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.shopuserprofile.save()
