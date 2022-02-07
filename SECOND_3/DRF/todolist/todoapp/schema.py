import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from .models import Project, Todo


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        fields = '__all__'


class ProjectType(DjangoObjectType):
    class Meta:
        model = Project
        fields = '__all__'


class TodoType(DjangoObjectType):
    class Meta:
        model = Todo
        fields = '__all__'


class Query(graphene.ObjectType):
    hello = graphene.String(default_value='Hi!')

    all_users = graphene.List(UserType)

    def resolve_all_users(root, info):
        return get_user_model().objects.all()

    all_projects = graphene.List(ProjectType)

    def resolve_all_projects(root, info):
        return Project.objects.all()

    all_todos = graphene.List(TodoType)

    def resolve_all_todos(root, info):
        return Todo.objects.all()

    # запрос, по которому можно получить все связи:
    # {
    #     allUsers
    #     {
    #         id
    #         firstName
    #     }
    #     allTodos
    #     {
    #         id
    #         todoText
    #         project
    #         {
    #             id
    #         }
    #     }
    #     allProjects
    #     {
    #         id
    #         projectName
    #         assignedUsers
    #         {
    #             id
    #         }
    #     }
    # }

schema = graphene.Schema(query=Query)
