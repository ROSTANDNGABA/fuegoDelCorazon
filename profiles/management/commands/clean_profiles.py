from django.core.management.base import BaseCommand
from profiles.models import StudentProfile
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Vérifie et nettoie les profils en double'

    def handle(self, *args, **options):
        username = 'rostand'
        try:
            user = User.objects.get(username=username)
            self.stdout.write(f'Utilisateur trouvé: {user.username}')
            
            profiles = StudentProfile.objects.filter(user=user)
            self.stdout.write(f'Nombre de profils pour {username}: {profiles.count()}')
            
            if profiles.count() > 1:
                self.stdout.write('Suppression des profils en double...')
                # Garder le premier profil, supprimer les autres
                first_profile = profiles.first()
                profiles.exclude(id=first_profile.id).delete()
                self.stdout.write(self.style.SUCCESS(f'Profil conservé: {first_profile}'))
            elif profiles.count() == 1:
                self.stdout.write(self.style.SUCCESS('Un seul profil trouvé - OK'))
            else:
                self.stdout.write(self.style.WARNING('Aucun profil trouvé'))
                
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Utilisateur {username} non trouvé'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erreur: {str(e)}'))
