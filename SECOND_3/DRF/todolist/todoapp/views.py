from djangorestframework_camel_case.render import CamelCaseJSONRenderer, CamelCaseBrowsableAPIRenderer
from rest_framework.viewsets import ModelViewSet
from .models import Project, Todo
from .serializers import ProjectModelSerializer, TodoModelSerializer

from django.shortcuts import render


# Create your views here.

class ProjectModelViewSet(ModelViewSet):
    renderer_classes = [CamelCaseJSONRenderer, CamelCaseBrowsableAPIRenderer]
    queryset = Project.objects.all()
    serializer_class = ProjectModelSerializer


class TodoModelViewSet(ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoModelSerializer
