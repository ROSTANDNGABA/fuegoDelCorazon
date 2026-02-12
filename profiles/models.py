from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Homme'),
        ('F', 'Femme'),
        ('A', 'Autre'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='A')
    field_of_study = models.CharField(max_length=100)
    bio = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
