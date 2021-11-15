from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlunparse, urlencode

import requests
from django.utils.timezone import now
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = urlunparse(('https',
                          'api.vk.com',
                          '/method/users.get',
                          None,
                          urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about')),
                                                access_token=response['access_token'],
                                                v='5.131')),
                          None
                          ))

    resp = requests.get(api_url)
    if resp.status_code != 200:
        return

    data = resp.json()['response'][0]
    if data['sex']:
        user.shopuserprofile.sex = ShopUserProfile.SexChoices.MALE if data['sex'] == 2 else ShopUserProfile.SexChoices.FEMALE

    if data['about']:
        user.shopuserprofile.about_me = data['about']

    if data['bdate']:
        bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()

        age = now().date().year - bdate.year
        # if age < 100:  # п.4 ДЗ
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')
        user.age = age

    user.save()
