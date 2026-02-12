from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q, Count
from profiles.models import StudentProfile
from questions.models import Answer, Question
from .models import Match

@login_required
def matches(request):
    # DEBUG: Afficher les informations de l'utilisateur
    print(f"DEBUG: Utilisateur connecté: {request.user.username}")
    
    # Récupérer toutes les questions existantes
    total_questions = Question.objects.count()
    print(f"DEBUG: Total questions: {total_questions}")
    
    # Vérifier les réponses de l'utilisateur
    user_answers = Answer.objects.filter(user=request.user)
    answered_questions = user_answers.count()
    print(f"DEBUG: Réponses de l'utilisateur: {answered_questions}")
    
    # Si l'utilisateur n'a répondu à aucune question
    if answered_questions == 0:
        print("DEBUG: Redirection vers no_answers.html")
        return render(request, 'matches/no_answers.html')
    
    # Si l'utilisateur n'a pas répondu à TOUTES les questions
    if answered_questions < total_questions:
        print("DEBUG: Redirection vers incomplete_answers.html")
        context = {
            'answered_questions': answered_questions,
            'total_questions': total_questions,
            'remaining_questions': total_questions - answered_questions,
            'completion_percentage': round((answered_questions / total_questions) * 100, 1)
        }
        return render(request, 'matches/incomplete_answers.html', context)
    
    # Get current user's profile
    try:
        current_profile = StudentProfile.objects.get(user=request.user)
        current_gender = current_profile.gender
        print(f"DEBUG: Profil trouvé, genre: {current_gender}")
    except StudentProfile.DoesNotExist:
        print("DEBUG: Pas de profil, redirection vers no_answers.html")
        return render(request, 'matches/no_answers.html')
    
    # Get all other users who have answered ALL questions and have profiles
    # Utiliser une sous-requête pour éviter les problèmes
    users_with_all_answers = User.objects.filter(
        ~Q(id=request.user.id),
        studentprofile__isnull=False
    ).annotate(
        answer_count=Count('answer')
    ).filter(
        answer_count=total_questions
    )
    
    print(f"DEBUG: Autres utilisateurs avec toutes les réponses: {users_with_all_answers.count()}")
    
    matches_list = []
    
    for other_user in users_with_all_answers:
        # Check if other user has a profile
        try:
            other_profile = StudentProfile.objects.get(user=other_user)
            other_gender = other_profile.gender
            print(f"DEBUG: Autre utilisateur {other_user.username}, genre: {other_gender}")
        except StudentProfile.DoesNotExist:
            continue
        
        # Skip matching between same gender
        if current_gender == other_gender:
            print(f"DEBUG: Skip {other_user.username} - même genre")
            continue
        
        # Allow matching with 'A' (Autre) for both sides
        # But still exclude same gender matching
        # This allows: M↔A, F↔A, A↔M, A↔F
        # But excludes: M↔M, F↔F, A↔A
        
        other_answers = Answer.objects.filter(user=other_user)
        
        # Calculate compatibility score
        compatibility = calculate_compatibility(request.user, other_user)
        print(f"DEBUG: Compatibilité avec {other_user.username}: {compatibility}%")
        
        if compatibility > 0:
            matches_list.append({
                'user': other_user,
                'profile': other_profile,
                'compatibility_score': compatibility
            })
            print(f"DEBUG: Match ajouté: {other_user.username} ({compatibility}%)")
    
    # Sort by compatibility score (highest first)
    matches_list.sort(key=lambda x: x['compatibility_score'], reverse=True)
    
    print(f"DEBUG: Total matches trouvés: {len(matches_list)}")
    
    # Save matches to database
    Match.objects.filter(
        Q(user1=request.user) | Q(user2=request.user)
    ).delete()
    
    for match_data in matches_list[:20]:  # Keep top 20 matches
        Match.objects.create(
            user1=request.user,
            user2=match_data['user'],
            compatibility_score=match_data['compatibility_score']
        )
    
    context = {
        'matches': matches_list[:20],  # Show top 20 matches
        'total_matches': len(matches_list)
    }
    
    # If no matches found, show no_matches.html
    if not matches_list:
        print("DEBUG: Aucun match, redirection vers no_matches.html")
        return render(request, 'matches/no_matches.html', context)
    
    print("DEBUG: Affichage de matches.html")
    return render(request, 'matches/matches.html', context)

def calculate_compatibility(user1, user2):
    """Calculate compatibility score between two users based on their answers"""
    answers1 = Answer.objects.filter(user=user1)
    answers2 = Answer.objects.filter(user=user2)
    
    # Create dictionaries for quick lookup
    answers1_dict = {a.question_id: a.value for a in answers1}
    answers2_dict = {a.question_id: a.value for a in answers2}
    
    # Find common questions
    common_questions = set(answers1_dict.keys()) & set(answers2_dict.keys())
    
    if not common_questions:
        return 0
    
    # Calculate compatibility using multiple methods for better accuracy
    total_exact_matches = 0
    total_close_matches = 0
    total_weighted_score = 0
    max_possible_score = 0
    
    for question_id in common_questions:
        val1 = answers1_dict[question_id]
        val2 = answers2_dict[question_id]
        
        # Exact match (full points)
        if val1 == val2:
            total_exact_matches += 1
            total_weighted_score += 10
        # Close match (difference of 1) - partial points
        elif abs(val1 - val2) == 1:
            total_close_matches += 1
            total_weighted_score += 7
        # Moderate match (difference of 2) - fewer points
        elif abs(val1 - val2) == 2:
            total_weighted_score += 4
        # Distant match (difference of 3) - minimal points
        elif abs(val1 - val2) == 3:
            total_weighted_score += 2
        # Very distant (difference of 4) - very minimal points
        else:
            total_weighted_score += 1
        
        max_possible_score += 10  # Maximum per question
    
    # Calculate different compatibility metrics
    num_questions = len(common_questions)
    
    # Method 1: Exact match percentage
    exact_match_percentage = (total_exact_matches / num_questions) * 100
    
    # Method 2: Weighted score (more nuanced)
    weighted_compatibility = (total_weighted_score / max_possible_score) * 100
    
    # Method 3: Inverse distance (original method improved)
    total_distance = 0
    for question_id in common_questions:
        diff = abs(answers1_dict[question_id] - answers2_dict[question_id])
        total_distance += diff
    
    max_possible_distance = num_questions * 4
    distance_compatibility = max(0, (max_possible_distance - total_distance) / max_possible_distance * 100)
    
    # Combine all methods for a more accurate score
    # Weighted more towards exact matches and weighted scoring
    final_compatibility = (
        exact_match_percentage * 0.4 +      # 40% weight on exact matches
        weighted_compatibility * 0.4 +        # 40% weight on nuanced scoring
        distance_compatibility * 0.2             # 20% weight on distance method
    )
    
    # Bonus for having many exact matches
    if total_exact_matches >= num_questions * 0.8:  # 80%+ exact matches
        final_compatibility = min(100, final_compatibility + 5)  # 5% bonus
    
    return round(final_compatibility, 2)
