from django.core.management.base import BaseCommand
from questions.models import Question

class Command(BaseCommand):
    help = 'Crée des questions romantiques pour le questionnaire'

    def handle(self, *args, **options):
        # Supprimer les questions existantes
        Question.objects.all().delete()
        
        # Créer les questions romantiques avec leurs réponses personnalisées
        questions_data = [
            (1, "Crois-tu au coup de foudre dès le premier regard ?"),
            (2, "Pour toi, l'amour doit-il être passionnel ou plutôt stable et rassurant ?"),
            (3, "Aimes-tu recevoir souvent des messages romantiques de ton/ta partenaire ?"),
            (4, "Est-ce important pour toi de passer beaucoup de temps ensemble dans un couple ?"),
            (5, "Penses-tu que la communication est la clé d'une relation durable ?"),
            (6, "Te sens-tu à l'aise d'exprimer tes sentiments sans retenue ?"),
            (7, "Préfères-tu une relation exclusive et très engagée ?"),
            (8, "Les petites attentions du quotidien comptent-elles plus que les grands cadeaux ?"),
            (9, "Aimes-tu les surprises romantiques (dîners, lettres, sorties imprévues) ?"),
            (10, "Pour toi, l'amour doit-il inclure une grande complicité amicale ?"),
            (11, "Est-ce important que ton/ta partenaire partage tes valeurs et principes ?"),
            (12, "Te projettes-tu facilement dans une relation à long terme ?"),
            (13, "Le soutien émotionnel est-il essentiel pour toi dans un couple ?"),
            (14, "Aimes-tu montrer ton affection en public ?"),
            (15, "Penses-tu que la confiance totale est indispensable dans une relation ?"),
            (16, "Préfères-tu résoudre les conflits par le dialogue calme ?"),
            (17, "L'amour doit-il te rendre meilleur(e) chaque jour ?"),
            (18, "Est-ce important pour toi de célébrer les dates importantes ?"),
            (19, "Penses-tu que deux personnes très différentes peuvent être compatibles ?"),
            (20, "Te vois-tu construire un avenir sérieux avec la bonne personne ?"),
        ]
        
        for order, text in questions_data:
            Question.objects.create(
                text=text,
                order=order
            )
            self.stdout.write(
                self.style.SUCCESS(f'Question {order} créée: {text[:50]}...')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'{len(questions_data)} questions romantiques créées avec succès!')
        )
