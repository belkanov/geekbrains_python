from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Project(models.Model):
    project_name = models.CharField(
        max_length=200,
        verbose_name=_('имя проекта'),
    )
    repo_url = models.URLField(
        max_length=4000,
        null=True,
        verbose_name=_('ссылка на репозиторий'),
    )
    assigned_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('назначенные пользователи'),
    )

    def __str__(self):
        return f'[{self.pk}] {self.project_name}'


class Todo(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        verbose_name=_('проект'),
    )
    todo_text = models.CharField(  # char, а не text потому что это все таки заметка, а не сочинение
        max_length=4000,
        null=True,
        verbose_name=_('текст заметки'),
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('автор заметки'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('дата создания'),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('дата обновления'),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('активно'),
    )
