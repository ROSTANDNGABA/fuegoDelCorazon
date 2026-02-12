from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.models import Count
from questions.models import Answer, Question

class Command(BaseCommand):
    help = 'Vérifier la progression des questionnaires des utilisateurs'

    def handle(self, *args, **options):
        print("=== PROGRESSION DES QUESTIONNAIRES ===")
        
        total_questions = Question.objects.count()
        print(f"Total de questions: {total_questions}")
        
        users = User.objects.all()
        print(f"\nProgression par utilisateur:")
        
        for user in users:
            answered_count = Answer.objects.filter(user=user).count()
            completion_percentage = (answered_count / total_questions) * 100 if total_questions > 0 else 0
            
            status = "✅ Complet" if answered_count == total_questions else "🔄 En cours"
            
            print(f"- {user.username}: {answered_count}/{total_questions} ({completion_percentage:.1f}%) {status}")
        
        print("\n=== UTILISATEURS PRÊTS POUR MATCHING ===")
        ready_users = User.objects.annotate(
            answer_count=Count('answer')
        ).filter(answer_count=total_questions)
        
        print(f"Utilisateurs ayant répondu à TOUTES les questions: {ready_users.count()}")
        for user in ready_users:
            print(f"- {user.username}")
        
        print("\n=== UTILISATEURS BLOQUÉS POUR MATCHING ===")
        blocked_users = User.objects.annotate(
            answer_count=Count('answer')
        ).exclude(answer_count=total_questions).exclude(answer_count=0)
        
        print(f"Utilisateurs ayant répondu PARTIELLEMENT: {blocked_users.count()}")
        for user in blocked_users:
            answered_count = Answer.objects.filter(user=user).count()
            remaining = total_questions - answered_count
            print(f"- {user.username}: {remaining} questions restantes")
