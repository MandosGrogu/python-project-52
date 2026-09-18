from django.db import models
from users.models import CustomUser
from statuses.models import Status
from labels.models import Label

class Task(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    author = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='authored_tasks')
    performer = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL, related_name='assigned_tasks')
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    labels = models.ManyToManyField(Label)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title