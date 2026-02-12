from django.db import models
from django.contrib.auth.models import User

class Match(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches_as_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches_as_user2')
    compatibility_score = models.DecimalField(max_digits=5, decimal_places=2)  # Percentage
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user1', 'user2']
        indexes = [
            models.Index(fields=['user1', 'compatibility_score']),
            models.Index(fields=['user2', 'compatibility_score']),
        ]

    def __str__(self):
        return f"{self.user1.username} ↔ {self.user2.username}: {self.compatibility_score}%"
