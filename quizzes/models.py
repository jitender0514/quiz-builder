from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Quizzes(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_quizzes")

    def __str__(self):
        return self.title
