from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from profiles.models import StudentProfile

class Command(BaseCommand):
    help = 'Tester la robustesse de la connexion'

    def handle(self, *args, **options):
        print("=== TEST DE ROBUSTESSE DE LA CONNEXION ===")
        
        # Créer un utilisateur sans profil
        if not User.objects.filter(username='test_no_profile').exists():
            user_no_profile = User.objects.create_user(
                username='test_no_profile',
                email='test@example.com',
                password='Test123456!'
            )
            print("✅ Utilisateur sans profil créé: test_no_profile / Test123456!")
        else:
            print("ℹ️ L'utilisateur test_no_profile existe déjà")
        
        # Créer un utilisateur avec profil incomplet
        if not User.objects.filter(username='test_incomplete').exists():
            user_incomplete = User.objects.create_user(
                username='test_incomplete',
                email='test2@example.com',
                password='Test123456!'
            )
            # Créer un profil incomplet
            StudentProfile.objects.create(
                user=user_incomplete,
                age=25,
                gender='M',
                field_of_study=''  # Vide pour rendre le profil incomplet
            )
            print("✅ Utilisateur avec profil incomplet créé: test_incomplete / Test123456!")
        else:
            print("ℹ️ L'utilisateur test_incomplete existe déjà")
        
        # Créer un utilisateur avec profil complet
        if not User.objects.filter(username='test_complete').exists():
            user_complete = User.objects.create_user(
                username='test_complete',
                email='test3@example.com',
                password='Test123456!'
            )
            # Créer un profil complet
            StudentProfile.objects.create(
                user=user_complete,
                age=22,
                gender='F',
                field_of_study='Informatique',
                bio='Utilisateur de test avec profil complet'
            )
            print("✅ Utilisateur avec profil complet créé: test_complete / Test123456!")
        else:
            print("ℹ️ L'utilisateur test_complete existe déjà")
        
        print("\n=== UTILISATEURS DE TEST DISPONIBLES ===")
        users = User.objects.all()
        for user in users:
            try:
                profile = StudentProfile.objects.get(user=user)
                profile_status = "Complet" if profile.age and profile.gender and profile.field_of_study else "Incomplet"
                print(f"- {user.username}: Profil {profile_status}")
            except StudentProfile.DoesNotExist:
                print(f"- {user.username}: Aucun profil")
        
        print("\n=== SCÉNARIOS DE TEST ===")
        print("1. Essayez de vous connecter avec un nom d'utilisateur qui n'existe pas")
        print("2. Essayez de vous connecter avec test_no_profile (devrait rediriger vers création de profil)")
        print("3. Essayez de vous connecter avec test_incomplete (devrait rediriger vers édition de profil)")
        print("4. Essayez de vous connecter avec test_complete (devrait rediriger vers accueil)")
        print("5. Essayez avec un mot de passe incorrect")
