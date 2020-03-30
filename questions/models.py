from django.db import models
from quizzes.models import Quizzes

# Create your models here.


class Questions(models.Model):
    question = models.CharField(max_length=255, blank=False, null=False)
    quiz = models.ForeignKey(Quizzes, on_delete=models.CASCADE, related_name="quiz_questions")

    def __str__(self):
        return self.question
