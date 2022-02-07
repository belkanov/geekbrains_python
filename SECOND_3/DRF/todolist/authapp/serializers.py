from django.contrib.auth import get_user_model
from rest_framework.serializers import HyperlinkedModelSerializer


class UserModelSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['url', 'username', 'first_name', 'last_name', 'email']


class UserModelSerializerV2(HyperlinkedModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['url', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser']
