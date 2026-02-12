from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from profiles.models import StudentProfile
from questions.models import Answer
from matching.views import calculate_compatibility

class Command(BaseCommand):
    help = 'Tester en détail le calcul de compatibilité'

    def handle(self, *args, **options):
        print("=== TEST DÉTAILLÉ DE COMPATIBILITÉ ===")
        
        # Prendre deux utilisateurs avec des réponses différentes
        users = User.objects.filter(
            studentprofile__isnull=False,
            answer__isnull=False
        ).distinct()[:2]
        
        if len(users) < 2:
            print("❌ Pas assez d'utilisateurs pour tester")
            return
        
        user1, user2 = users[0], users[1]
        
        print(f"\nTest entre: {user1.username} et {user2.username}")
        
        # Récupérer les réponses
        answers1 = Answer.objects.filter(user=user1)
        answers2 = Answer.objects.filter(user=user2)
        
        answers1_dict = {a.question_id: a.value for a in answers1}
        answers2_dict = {a.question_id: a.value for a in answers2}
        
        common_questions = set(answers1_dict.keys()) & set(answers2_dict.keys())
        
        print(f"\nQuestions communes: {len(common_questions)}")
        
        # Analyser chaque question
        exact_matches = 0
        close_matches = 0
        total_diff = 0
        
        print("\nAnalyse détaillée:")
        for i, q_id in enumerate(sorted(common_questions), 1):
            val1 = answers1_dict[q_id]
            val2 = answers2_dict[q_id]
            diff = abs(val1 - val2)
            total_diff += diff
            
            if val1 == val2:
                exact_matches += 1
                match_type = "✅ EXACT"
                points = 10
            elif diff == 1:
                close_matches += 1
                match_type = "🟡 PROCHE"
                points = 7
            elif diff == 2:
                match_type = "🟡 MOYEN"
                points = 4
            elif diff == 3:
                match_type = "🟡 LOIN"
                points = 2
            else:
                match_type = "❌ TRÈS LOIN"
                points = 1
            
            print(f"  Q{i}: {val1} vs {val2} | diff={diff} | {match_type} | pts={points}")
        
        # Calculer le score final
        final_score = calculate_compatibility(user1, user2)
        
        print(f"\n📊 RÉSULTATS:")
        print(f"  Matches exacts: {exact_matches}/{len(common_questions)} ({exact_matches/len(common_questions)*100:.1f}%)")
        print(f"  Matches proches: {close_matches}")
        print(f"  Différence totale: {total_diff}")
        print(f"  Score final: {final_score}%")
        
        # Vérifier la cohérence
        max_possible = len(common_questions) * 10
        actual_score = (exact_matches * 10 + close_matches * 7) / max_possible * 100
        print(f"  Score pondéré: {actual_score:.2f}%")
