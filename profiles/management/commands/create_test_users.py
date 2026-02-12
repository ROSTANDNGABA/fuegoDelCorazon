from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from profiles.models import StudentProfile
from questions.models import Answer, Question
import random

class Command(BaseCommand):
    help = 'Créer des utilisateurs de test avec des réponses complètes'

    def handle(self, *args, **options):
        # Créer des utilisateurs de test avec réponses
        test_users = [
            ('pierre', 'M', 25, 'Informatique', 'Passionné de sport et de voyages'),
            ('lucas', 'M', 23, 'Marketing', 'Créatif et aventurier'),
            ('marc', 'M', 27, 'Finance', 'Sérieux mais romantique'),
            ('emma', 'F', 22, 'Design', 'Artistique et rêveuse'),
            ('sophie', 'F', 24, 'Psychologie', 'Empathique et attentive'),
        ]
        
        questions = list(Question.objects.all())
        
        for username, gender, age, field, bio in test_users:
            # Créer l'utilisateur
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(f'Utilisateur créé: {username}')
            
            # Créer le profil
            profile, created = StudentProfile.objects.get_or_create(
                user=user,
                defaults={
                    'age': age,
                    'gender': gender,
                    'field_of_study': field,
                    'bio': bio
                }
            )
            if created:
                self.stdout.write(f'Profil créé pour: {username}')
            
            # Supprimer les anciennes réponses
            Answer.objects.filter(user=user).delete()
            
            # Créer des réponses aléatoires mais cohérentes
            for question in questions:
                # Réponses plus variées pour créer des compatibilités différentes
                if username == 'pierre':  # Très romantique
                    base_score = random.randint(3, 5)
                elif username == 'lucas':  # Moyennement romantique
                    base_score = random.randint(2, 4)
                elif username == 'marc':  # Peu romantique mais stable
                    base_score = random.randint(1, 3)
                elif username == 'emma':  # Très romantique
                    base_score = random.randint(4, 5)
                elif username == 'sophie':  # Moyennement romantique
                    base_score = random.randint(2, 4)
                else:
                    base_score = random.randint(1, 5)
                
                Answer.objects.create(
                    user=user,
                    question=question,
                    value=base_score
                )
            
            self.stdout.write(f'20 réponses créées pour: {username}')
        
        self.stdout.write(self.style.SUCCESS('Utilisateurs de test créés avec succès!'))
        self.stdout.write('Vous pouvez maintenant voir des matches!')
