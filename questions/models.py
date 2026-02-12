from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    text = models.TextField()
    order = models.PositiveIntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Question {self.order}: {self.text[:50]}..."

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    value = models.PositiveIntegerField()  # 1-5 scale
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'question']

    def __str__(self):
        return f"{self.user.username} - Q{self.question.order}: {self.value}"
