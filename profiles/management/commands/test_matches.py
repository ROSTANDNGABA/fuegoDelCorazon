from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from profiles.models import StudentProfile
from questions.models import Answer
from matching.views import calculate_compatibility

class Command(BaseCommand):
    help = 'Tester les matches pour rostand'

    def handle(self, *args, **options):
        # Récupérer rostand
        rostand = User.objects.get(username='rostand')
        rostand_profile = StudentProfile.objects.get(user=rostand)
        
        self.stdout.write(f'Test des matches pour {rostand.username} (genre: {rostand_profile.gender})')
        
        # Récupérer tous les autres utilisateurs avec profils complets
        other_users = User.objects.exclude(id=rostand.id).filter(studentprofile__isnull=False)
        
        matches_found = []
        
        for other_user in other_users:
            try:
                other_profile = StudentProfile.objects.get(user=other_user)
                other_answers = Answer.objects.filter(user=other_user)
                
                # Vérifier si l'autre utilisateur a 20 réponses
                if other_answers.count() != 20:
                    self.stdout.write(f'{other_user.username}: seulement {other_answers.count()} réponses (ignoré)')
                    continue
                
                # Vérifier la compatibilité de genre
                can_match = False
                if rostand_profile.gender == 'A':
                    can_match = other_profile.gender != 'A'
                elif other_profile.gender == 'A':
                    can_match = True
                else:
                    can_match = rostand_profile.gender != other_profile.gender
                
                if not can_match:
                    self.stdout.write(f'{other_user.username}: genre incompatible ({other_profile.gender})')
                    continue
                
                # Calculer la compatibilité
                compatibility = calculate_compatibility(rostand, other_user)
                
                self.stdout.write(f'{other_user.username}: {compatibility}% de compatibilité ({other_profile.gender}, {other_profile.age} ans)')
                
                if compatibility > 0:
                    matches_found.append({
                        'user': other_user,
                        'profile': other_profile,
                        'compatibility_score': compatibility
                    })
                    
            except Exception as e:
                self.stdout.write(f'Erreur avec {other_user.username}: {str(e)}')
        
        # Trier par compatibilité
        matches_found.sort(key=lambda x: x['compatibility_score'], reverse=True)
        
        self.stdout.write(f'\n=== RÉSULTAT FINAL ===')
        self.stdout.write(f'Total matches trouvés: {len(matches_found)}')
        
        for i, match in enumerate(matches_found, 1):
            self.stdout.write(f'{i}. {match["user"].username}: {match["compatibility_score"]}%')
        
        if matches_found:
            self.stdout.write(self.style.SUCCESS('✅ Matches trouvés! La page devrait fonctionner.'))
        else:
            self.stdout.write(self.style.WARNING('❌ Aucun match trouvé.'))
