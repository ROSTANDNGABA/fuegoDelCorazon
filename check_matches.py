from django.contrib.auth.models import User
from profiles.models import StudentProfile
from questions.models import Answer
from django.db.models import Count

# Statistiques des utilisateurs
total_users = User.objects.count()
users_with_profiles = StudentProfile.objects.count()

# Utilisateurs ayant répondu à toutes les questions (20 questions)
users_with_all_answers = User.objects.annotate(
    answer_count=Count('answer')
).filter(answer_count=20).count()

print(f'Total users: {total_users}')
print(f'Users with profiles: {users_with_profiles}')
print(f'Users with all answers: {users_with_all_answers}')

# Détails des utilisateurs avec profils
print('\nUtilisateurs avec profils:')
for profile in StudentProfile.objects.all():
    user = profile.user
    answers_count = Answer.objects.filter(user=user).count()
    print(f'- {user.username}: {answers_count} réponses, genre: {profile.gender}')

# Vérifier les matches potentiels pour rostand
print('\nAnalyse des matches pour rostand:')
rostand = User.objects.get(username='rostand')
rostand_profile = StudentProfile.objects.get(user=rostand)
rostand_gender = rostand_profile.gender

print(f'Genre de rostand: {rostand_gender}')

other_users = User.objects.exclude(id=rostand.id).filter(studentprofile__isnull=False)
print(f'Autres utilisateurs avec profil: {other_users.count()}')

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
        
        print(f'- {user.username}: {answers_count} réponses, genre: {profile.gender}, match possible: {can_match}')
    except:
        print(f'- {user.username}: pas de profil')
