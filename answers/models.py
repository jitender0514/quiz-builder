from django.db import models
from questions.models import Questions

# Create your models here.


class Answers(models.Model):
    answer = models.TextField()
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name="question_answers")
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer
