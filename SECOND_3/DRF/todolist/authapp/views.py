from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from .models import User
from .serializers import UserModelSerializer

from django.shortcuts import render


# Create your views here.

class UserModelViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

    # потесил в постмане:
    # - GET ОК http://127.0.0.1:8000/api/users/
    # - GET ОК http://127.0.0.1:8000/api/users/4/
    # - PUT ОК, ругается, если не все поля
    # - PATCH OK, с одним полем
    # - POST not allowed
    # - DEL not allowed
