from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate
from .views import UserModelViewSet
from .models import User


class TestUserViewSet(TestCase):

    def test_get_users_not_auth(self):
        factory = APIRequestFactory()
        request = factory.get('/api/users/')
        view = UserModelViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # AnonReadOnly выключен

    def test_get_users_auth(self):
        factory = APIRequestFactory()
        request = factory.get('/api/users/')
        view = UserModelViewSet.as_view({'get': 'list'})
        admin = User.objects.create_superuser('admin', 'admin@admin.com', '123')
        force_authenticate(request, admin)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
