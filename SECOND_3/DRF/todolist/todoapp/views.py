from djangorestframework_camel_case.render import CamelCaseJSONRenderer, CamelCaseBrowsableAPIRenderer
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from .models import Project, Todo
from .serializers import ProjectModelSerializer, TodoModelSerializer


# Create your views here.

class ProjectPageNumberPagination(PageNumberPagination):
    page_size = 10


class TodoPageNumberPagination(PageNumberPagination):
    page_size = 20


class ProjectModelViewSet(ModelViewSet):
    renderer_classes = [CamelCaseJSONRenderer, CamelCaseBrowsableAPIRenderer]
    queryset = Project.objects.all().order_by('pk')  # сортировка, чтобы не было UnorderedObjectListWarning в связке с пагинацией
    serializer_class = ProjectModelSerializer
    pagination_class = ProjectPageNumberPagination

    # GET, OK http://127.0.0.1:8000/api/projects/?name=_3
    def get_queryset(self):
        projects = self.queryset
        if project_name := self.request.query_params.get('name'):
            projects = projects.filter(project_name__contains=project_name)
        return projects


class TodoModelViewSet(ModelViewSet):
    queryset = Todo.objects.filter(is_active=True).order_by('pk')
    serializer_class = TodoModelSerializer
    pagination_class = TodoPageNumberPagination
    filterset_fields = ['project']  # GET, OK http://127.0.0.1:8000/api/todos/?project=2

    def perform_destroy(self, instance: Todo):
        instance.is_active = False
        instance.save()
