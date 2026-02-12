from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from profiles.models import StudentProfile

class Command(BaseCommand):
    help = 'Vérifier les comptes utilisateurs existants'

    def handle(self, *args, **options):
        print("=== VÉRIFICATION DES COMPTES UTILISATEURS ===")
        
        users = User.objects.all()
        print(f"Total utilisateurs: {users.count()}")
        
        for user in users:
            print(f"\n--- {user.username} ---")
            print(f"Email: {user.email}")
            print(f"Actif: {user.is_active}")
            print(f"Staff: {user.is_staff}")
            
            try:
                profile = StudentProfile.objects.get(user=user)
                print(f"✅ Profil trouvé:")
                print(f"   Âge: {profile.age}")
                print(f"   Genre: {profile.get_gender_display()}")
                print(f"   Étude: {profile.field_of_study}")
                print(f"   Bio: {profile.bio[:50] if profile.bio else 'Non'}...")
                
                # Vérifier si le profil est complet
                is_complete = bool(profile.age and profile.gender and profile.field_of_study)
                print(f"   Complet: {'Oui' if is_complete else 'Non'}")
                
            except StudentProfile.DoesNotExist:
                print("❌ Aucun profil")
        
        print("\n=== TEST DE CONNEXION ===")
        print("Essayez de vous connecter avec vos identifiants habituels.")
        print("Si ça ne marche pas, vérifiez les logs du serveur pour les messages de debug.")
