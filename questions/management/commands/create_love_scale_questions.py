from django.core.management.base import BaseCommand
from questions.models import Question

class Command(BaseCommand):
    help = 'Ajouter des questions de compatibilité amoureuse avec échelle 1-5'

    def handle(self, *args, **options):
        # Supprimer les questions existantes
        Question.objects.all().delete()
        
        questions_data = [
            # Vision de l'amour
            ("Crois-tu au coup de foudre dès le premier regard ?", 1),
            ("Pour toi, l'amour doit-il être passionnel ou plutôt stable et rassurant ?", 2),
            ("Aimes-tu recevoir souvent des messages romantiques de ton/ta partenaire ?", 3),
            ("Est-ce important pour toi de passer beaucoup de temps ensemble dans un couple ?", 4),
            
            # Communication & émotions
            ("Penses-tu que la communication est la clé d'une relation durable ?", 5),
            ("Te sens-tu à l'aise d'exprimer tes sentiments sans retenue ?", 6),
            ("Préfères-tu résoudre les conflits par le dialogue calme ?", 7),
            
            # Engagement & exclusivité
            ("Préfères-tu une relation exclusive et très engagée ?", 8),
            ("Te projettes-tu facilement dans une relation à long terme ?", 9),
            ("Te vois-tu construire un avenir sérieux avec la bonne personne ?", 10),
            
            # Attentions & romance
            ("Les petites attentions du quotidien comptent-elles plus que les grands cadeaux ?", 11),
            ("Aimes-tu les surprises romantiques (dîners, lettres, sorties imprévues) ?", 12),
            ("Est-ce important pour toi de célébrer les dates importantes ?", 13),
            
            # Valeurs & compatibilité
            ("Pour toi, l'amour doit-il inclure une grande complicité amicale ?", 14),
            ("Est-ce important que ton/ta partenaire partage tes valeurs et principes ?", 15),
            ("Penses-tu que deux personnes très différentes peuvent être compatibles ?", 16),
            
            # Soutien & affection
            ("Le soutien émotionnel est-il essentiel pour toi dans un couple ?", 17),
            ("Aimes-tu montrer ton affection en public ?", 18),
            
            # Confiance & croissance
            ("Penses-tu que la confiance totale est indispensable dans une relation ?", 19),
            ("L'amour doit-il te rendre meilleur(e) chaque jour ?", 20),
        ]
        
        # Créer les questions
        for i, (text, order) in enumerate(questions_data, 1):
            Question.objects.create(text=text, order=order)
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {len(questions_data)} love compatibility questions (scale 1-5)')
        )
