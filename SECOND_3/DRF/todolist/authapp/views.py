from rest_framework.viewsets import ModelViewSet
from .models import User
from .serializers import UserModelSerializer

from django.shortcuts import render


# Create your views here.

class UserModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
