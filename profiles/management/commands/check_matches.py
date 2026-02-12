from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from profiles.models import StudentProfile
from questions.models import Answer
from django.db.models import Count

class Command(BaseCommand):
    help = 'Vérifier les statistiques des utilisateurs et les matches potentiels'

    def handle(self, *args, **options):
        # Statistiques des utilisateurs
        total_users = User.objects.count()
        users_with_profiles = StudentProfile.objects.count()

        # Utilisateurs ayant répondu à toutes les questions (20 questions)
        users_with_all_answers = User.objects.annotate(
            answer_count=Count('answer')
        ).filter(answer_count=20).count()

        self.stdout.write(f'Total users: {total_users}')
        self.stdout.write(f'Users with profiles: {users_with_profiles}')
        self.stdout.write(f'Users with all answers: {users_with_all_answers}')

        # Détails des utilisateurs avec profils
        self.stdout.write('\nUtilisateurs avec profils:')
        for profile in StudentProfile.objects.all():
            user = profile.user
            answers_count = Answer.objects.filter(user=user).count()
            self.stdout.write(f'- {user.username}: {answers_count} réponses, genre: {profile.gender}')

        # Vérifier les matches potentiels pour rostand
        self.stdout.write('\nAnalyse des matches pour rostand:')
        rostand = User.objects.get(username='rostand')
        rostand_profile = StudentProfile.objects.get(user=rostand)
        rostand_gender = rostand_profile.gender

        self.stdout.write(f'Genre de rostand: {rostand_gender}')

        other_users = User.objects.exclude(id=rostand.id).filter(studentprofile__isnull=False)
        self.stdout.write(f'Autres utilisateurs avec profil: {other_users.count()}')

        potential_matches = 0
        for user in other_users:
            try:
                profile = StudentProfile.objects.get(user=user)
                answers_count = Answer.objects.filter(user=user).count()
                
                # Vérifier si le matching est possible selon le genre
                can_match = False
                if rostand_gender == 'A':
                    can_match = profile.gender != 'A'
                elif profile.gender == 'A':
                    can_match = True
                else:
                    can_match = rostand_gender != profile.gender
                
                if answers_count == 20 and can_match:
                    potential_matches += 1
                
                self.stdout.write(f'- {user.username}: {answers_count} réponses, genre: {profile.gender}, match possible: {can_match}')
            except:
                self.stdout.write(f'- {user.username}: pas de profil')
        
        self.stdout.write(f'\nMatches potentiels pour rostand: {potential_matches}')
        
        if potential_matches == 0:
            self.stdout.write(self.style.WARNING('Aucun match potentiel trouvé!'))
            self.stdout.write('Raisons possibles:')
            self.stdout.write('1. Pas d\'autres utilisateurs avec 20 réponses')
            self.stdout.write('2. Tous les autres utilisateurs ont le même genre')
            self.stdout.write('3. Les autres utilisateurs n\'ont pas de profil')
