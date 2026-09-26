from django.conf import settings
from django.db import models

from labels.models import Label
from statuses.models import Status


class Task(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.PROTECT, 
        related_name='authored_tasks'
        )
    performer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        blank=True,
        null=True, 
        on_delete=models.SET_NULL, 
        related_name='assigned_tasks'
        )
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    labels = models.ManyToManyField(Label)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title