from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from authapp.models import User
from .models import Project
from django.contrib.auth.models import Permission, Group

from mixer.backend.django import mixer


class TestProjectView(TestCase):
    def setUp(self):
        self.admin_username = 'admin'
        self.admin_password = 'qwerty'
        self.admin = User.objects.create_superuser(self.admin_username, email='admin@example.com', password=self.admin_password)

    def test_get_detail(self):
        project = Project.objects.create(project_name='test1', )
        client = APIClient()
        client.login(username=self.admin_username, password=self.admin_password)
        response = client.get(f'/api/projects/{project.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# с проектами проще работать, сделал отдельный класс из-за APITestCase
class TestProjectView2(APITestCase):
    def setUp(self):
        self.username = 'user1'
        self.password = 'qwerty'
        self.user = User.objects.create_user(self.username, email='user@example.com', password=self.password)
        # из-за DjangoModelPermissions
        add_project_permission = Permission.objects.get(content_type__app_label='todoapp', codename='change_project')
        self.user.user_permissions.add(add_project_permission)

    def test_create_todo_by_api(self):
        project = mixer.blend(Project)
        self.client.login(username=self.username, password=self.password)
        response = self.client.put(f'/api/projects/{project.id}/', {
            'project_name': 'test_project_name',
            'assigned_users': self.user.id
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['project_name'], 'test_project_name')
        self.assertEqual(response.data['assigned_users'], [self.user.id, ])

