from rest_framework.fields import empty
from rest_framework.serializers import HyperlinkedModelSerializer, ModelSerializer
from .models import Project, Todo


class ProjectModelSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class TodoModelSerializer(ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'


class TodoModelCreateSerializer(ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'project', 'todo_text']
        read_only_fields = ['id']

    def save(self, **kwargs):
        kwargs.update({
            'created_by': self.context['request'].user
        })
        return super().save(**kwargs)


