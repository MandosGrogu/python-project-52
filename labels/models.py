from django.db import models
from django.db.models import ProtectedError


class Label(models.Model):
    title = models.CharField(max_length=500, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        if self.task_set.exists():
            raise ProtectedError(
                "Невозможно удалить метку",
                self.task_set.all()
            )
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title