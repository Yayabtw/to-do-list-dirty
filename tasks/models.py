from django.db import models


class Task(models.Model):
    """Model representing a task in the to-do list."""

    title = models.CharField(max_length=200)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
