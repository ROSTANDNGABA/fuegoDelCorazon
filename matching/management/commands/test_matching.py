from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from profiles.models import StudentProfile
from questions.models import Answer
from matching.models import Match
from matching.views import calculate_compatibility

class Command(BaseCommand):
    help = 'Tester le matching entre utilisateurs'

    def handle(self, *args, **options):
        print("=== TEST DE MATCHING ===")
        
        # Récupérer tous les utilisateurs avec profils et réponses
        users = User.objects.filter(
            studentprofile__isnull=False,
            answer__isnull=False
        ).distinct()
        
        print(f"Utilisateurs éligibles: {users.count()}")
        
        # Tester le matching pour chaque paire
        for user1 in users:
            print(f"\n--- Matches pour {user1.username} ---")
            
            try:
                profile1 = StudentProfile.objects.get(user=user1)
                gender1 = profile1.gender
                print(f"Genre: {gender1}")
            except:
                continue
            
            matches_for_user1 = []
            
            for user2 in users:
                if user1.id == user2.id:
                    continue
                
                try:
                    profile2 = StudentProfile.objects.get(user=user2)
                    gender2 = profile2.gender
                except:
                    continue
                
                # Vérifier les règles de matching
                if gender1 == gender2:
                    print(f"  ❌ {user2.username}: même genre ({gender1}={gender2})")
                    continue
                
                print(f"  ✅ {user2.username}: genres compatibles ({gender1}≠{gender2})")
                
                # Calculer la compatibilité
                compatibility = calculate_compatibility(user1, user2)
                print(f"     Compatibilité: {compatibility}%")
                
                if compatibility > 0:
                    matches_for_user1.append({
                        'user': user2,
                        'compatibility': compatibility
                    })
            
            # Trier par compatibilité
            matches_for_user1.sort(key=lambda x: x['compatibility'], reverse=True)
            
            print(f"\n📊 Résultats pour {user1.username}:")
            for match in matches_for_user1[:3]:
                print(f"  {match['user'].username}: {match['compatibility']}%")
            
            if not matches_for_user1:
                print("  ❌ Aucun match trouvé")
