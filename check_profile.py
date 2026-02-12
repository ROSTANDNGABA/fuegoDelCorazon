from profiles.models import StudentProfile
from django.contrib.auth.models import User

# Récupérer l'utilisateur
user = User.objects.get(username='rostand')
print('User:', user)

# Vérifier si un profil existe
try:
    profile = StudentProfile.objects.get(user=user)
    print('Profile exists:', profile)
    profile.delete()
    print('Profile deleted')
except StudentProfile.DoesNotExist:
    print('No profile found')
