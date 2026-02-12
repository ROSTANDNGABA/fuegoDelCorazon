from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from profiles.models import StudentProfile
from questions.models import Answer

class Command(BaseCommand):
    help = 'Vérifier les profils et réponses des utilisateurs'

    def handle(self, *args, **options):
        print("=== VÉRIFICATION DES UTILISATEURS ===")
        
        users = User.objects.all()
        print(f"Total utilisateurs: {users.count()}")
        
        for user in users:
            print(f"\n--- Utilisateur: {user.username} ---")
            
            # Vérifier le profil
            try:
                profile = StudentProfile.objects.get(user=user)
                print(f"✅ Profil trouvé - Genre: {profile.get_gender_display()}, Âge: {profile.age}")
            except StudentProfile.DoesNotExist:
                print("❌ Pas de profil")
                continue
            
            # Vérifier les réponses
            answers = Answer.objects.filter(user=user)
            print(f"✅ {answers.count()} réponse(s) au questionnaire")
            
            if answers.exists():
                for answer in answers[:3]:  # Montrer les 3 premières
                    print(f"   Question {answer.question.order}: {answer.value}")
        
        print("\n=== UTILISATEURS AVEC PROFILS COMPLETS ===")
        complete_users = User.objects.filter(
            studentprofile__isnull=False,
            answer__isnull=False
        ).distinct()
        
        print(f"Utilisateurs avec profil + réponses: {complete_users.count()}")
        for user in complete_users:
            try:
                profile = StudentProfile.objects.get(user=user)
                print(f"- {user.username}: {profile.get_gender_display()}, {profile.age} ans")
            except:
                pass
