from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from .models import User
from .serializers import UserModelSerializer, UserModelSerializerV2

from django.shortcuts import render


# Create your views here.

class UserModelViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = User.objects.all().order_by('pk')
    serializer_class = UserModelSerializer

    def get_serializer_class(self):

        # ?version=2
        if self.request.version == '2':
            return UserModelSerializerV2
        return UserModelSerializer

