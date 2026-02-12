from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from profiles.models import StudentProfile
from questions.models import Answer

class Command(BaseCommand):
    help = 'Créer des utilisateurs de test pour le matching'

    def handle(self, *args, **options):
        print("=== CRÉATION D'UTILISATEURS DE TEST ===")
        
        # Utilisateur femme de test
        if not User.objects.filter(username='marie_test').exists():
            user_femme = User.objects.create_user(
                username='marie_test',
                email='marie@test.com',
                password='test123456'
            )
            
            profile_femme = StudentProfile.objects.create(
                user=user_femme,
                age=22,
                gender='F',
                field_of_study='Informatique',
                bio='Étudiante passionnée par les nouvelles technologies'
            )
            
            # Ajouter quelques réponses
            from questions.models import Question
            questions = Question.objects.all()[:10]
            for i, question in enumerate(questions, 1):
                Answer.objects.create(
                    user=user_femme,
                    question=question,
                    value=i % 5 + 1  # Réponses variées 1-5
                )
            
            print("✅ Utilisateur femme créé: marie_test / test123456")
        else:
            print("ℹ️ L'utilisateur marie_test existe déjà")
        
        print("\n=== UTILISATEURS DISPONIBLES ===")
        users = User.objects.filter(studentprofile__isnull=False).distinct()
        for user in users:
            try:
                profile = StudentProfile.objects.get(user=user)
                print(f"- {user.username}: {profile.get_gender_display()}, {profile.age} ans")
            except:
                pass
