from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import Question, Answer
import logging

logger = logging.getLogger(__name__)

@login_required
def questionnaire(request):
    try:
        questions = Question.objects.all().order_by('order')
        
        if request.method == 'POST':
            # Delete existing answers for this user
            Answer.objects.filter(user=request.user).delete()
            
            # Save new answers
            for question in questions:
                value = request.POST.get(f'question_{question.id}')
                if value:
                    Answer.objects.create(
                        user=request.user,
                        question=question,
                        value=int(value)
                    )
            
            messages.success(request, 'Vos réponses ont été enregistrées avec succès!')
            return redirect('questions:questionnaire')
        
        # Get existing answers and prepare them for template
        user_answers = {}
        for answer in Answer.objects.filter(user=request.user):
            user_answers[answer.question.id] = answer.value
        
        # Create a list of tuples (question, answer) for easier template access
        questions_with_answers = []
        for question in questions:
            questions_with_answers.append({
                'question': question,
                'answer': user_answers.get(question.id)
            })
        
        # Réponses personnalisées pour chaque question romantique
        choices_by_question = {
            1: [
                (1, 'Pas du tout'),
                (2, 'Plutôt non'),
                (3, 'Neutre'),
                (4, 'Plutôt oui'),
                (5, 'Totalement')
            ],
            2: [
                (1, 'Totalement stable'),
                (2, 'Plutôt stable'),
                (3, 'Un équilibre des deux'),
                (4, 'Plutôt passionnel'),
                (5, 'Très passionnel')
            ],
            3: [
                (1, 'Pas du tout'),
                (2, 'Rarement'),
                (3, 'De temps en temps'),
                (4, 'Souvent'),
                (5, 'Tout le temps')
            ],
            4: [
                (1, 'Pas important'),
                (2, 'Peu important'),
                (3, 'Modérément important'),
                (4, 'Important'),
                (5, 'Très important')
            ],
            5: [
                (1, 'Pas du tout'),
                (2, 'Peu importante'),
                (3, 'Moyennement importante'),
                (4, 'Importante'),
                (5, 'Essentielle')
            ],
            6: [
                (1, 'Pas du tout'),
                (2, 'Difficilement'),
                (3, 'Parfois'),
                (4, 'Souvent'),
                (5, 'Toujours')
            ],
            7: [
                (1, 'Pas du tout'),
                (2, 'Peu engagée'),
                (3, 'Moyennement engagée'),
                (4, 'Très engagée'),
                (5, 'Totalement exclusive')
            ],
            8: [
                (1, 'Pas du tout'),
                (2, 'Peu'),
                (3, 'Autant les deux'),
                (4, 'Oui'),
                (5, 'Beaucoup plus')
            ],
            9: [
                (1, 'Pas du tout'),
                (2, 'Peu'),
                (3, 'Moyennement'),
                (4, 'Beaucoup'),
                (5, 'Passionnément')
            ],
            10: [
                (1, 'Pas nécessaire'),
                (2, 'Peu importante'),
                (3, 'Importante'),
                (4, 'Très importante'),
                (5, 'Indispensable')
            ],
            11: [
                (1, 'Pas important'),
                (2, 'Peu important'),
                (3, 'Assez important'),
                (4, 'Très important'),
                (5, 'Essentiel')
            ],
            12: [
                (1, 'Pas du tout'),
                (2, 'Difficilement'),
                (3, 'Parfois'),
                (4, 'Facilement'),
                (5, 'Très facilement')
            ],
            13: [
                (1, 'Pas important'),
                (2, 'Peu important'),
                (3, 'Important'),
                (4, 'Très important'),
                (5, 'Indispensable')
            ],
            14: [
                (1, 'Pas du tout'),
                (2, 'Rarement'),
                (3, 'Parfois'),
                (4, 'Souvent'),
                (5, 'Tout le temps')
            ],
            15: [
                (1, 'Pas du tout'),
                (2, 'Peu'),
                (3, 'Importante'),
                (4, 'Très importante'),
                (5, 'Absolument indispensable')
            ],
            16: [
                (1, 'Pas du tout'),
                (2, 'Rarement'),
                (3, 'Parfois'),
                (4, 'Souvent'),
                (5, 'Toujours')
            ],
            17: [
                (1, 'Pas du tout'),
                (2, 'Peu'),
                (3, 'Moyennement'),
                (4, 'Oui'),
                (5, 'Absolument')
            ],
            18: [
                (1, 'Pas important'),
                (2, 'Peu important'),
                (3, 'Important'),
                (4, 'Très important'),
                (5, 'Essentiel')
            ],
            19: [
                (1, 'Pas du tout'),
                (2, 'Peu probable'),
                (3, 'Peut-être'),
                (4, 'Probable'),
                (5, 'Tout à fait')
            ],
            20: [
                (1, 'Pas du tout'),
                (2, 'Difficilement'),
                (3, 'Peut-être'),
                (4, 'Oui'),
                (5, 'Certainement')
            ]
        }
        
        context = {
            'questions_with_answers': questions_with_answers,
            'total_questions': questions.count(),
            'completed': len(user_answers) == questions.count(),
            'progress_percentage': int((len(user_answers) / questions.count()) * 100) if questions.count() > 0 else 0,
            'choices_by_question': choices_by_question
        }
        
        return render(request, 'questions/questionnaire.html', context)
        
    except Exception as e:
        logger.error(f"Erreur dans la vue questionnaire: {str(e)}")
        messages.error(request, f"Une erreur est survenue: {str(e)}")
        return render(request, 'questions/questionnaire.html', {
            'questions_with_answers': [],
            'total_questions': 0,
            'completed': False,
            'progress_percentage': 0,
            'choices_by_question': {},
            'error': str(e)
        })

@staff_member_required
def view_answers(request):
    """Vue simple pour voir les réponses (accessible uniquement au staff)"""
    answers = Answer.objects.all().select_related('user', 'question').order_by('user__username', 'question__order')
    
    context = {
        'answers': answers
    }
    
    return render(request, 'questions/view_answers.html', context)
