from django.core.management.base import BaseCommand
from questions.models import Question

class Command(BaseCommand):
    help = 'Ajouter des questions sur les relations amoureuses'

    def handle(self, *args, **options):
        # Supprimer les questions existantes
        Question.objects.all().delete()
        
        questions_data = [
            # Communication & émotions
            ("Croyez-vous qu'une relation amoureuse doit être basée sur la confiance ?", 1),
            ("Pensez-vous que la communication est essentielle dans un couple ?", 2),
            ("Recherchez-vous une relation sérieuse et durable ?", 3),
            
            # Engagement & efforts
            ("Êtes-vous prêt(e) à faire des efforts pour construire une relation ?", 4),
            ("Pensez-vous qu'un couple doit grandir et évoluer ensemble ?", 5),
            
            # Communication & émotions (suite)
            ("Exprimez-vous facilement vos sentiments à la personne que vous aimez ?", 6),
            ("Prenez-vous le temps d'écouter et de comprendre les émotions de votre partenaire ?", 7),
            ("Préférez-vous discuter calmement plutôt que vous disputer en cas de désaccord ?", 8),
            ("Vous sentez-vous à l'aise pour parler de vos peurs ou de vos doutes ?", 9),
            
            # Honnêteté & fidélité
            ("L'honnêteté est-elle une valeur importante pour vous en amour ?", 10),
            ("Vous considérez-vous comme une personne fidèle ?", 11),
            
            # Respect & soutien
            ("Respectez-vous l'espace personnel de votre partenaire ?", 12),
            ("Soutenez-vous votre partenaire dans les moments difficiles ?", 13),
            ("Êtes-vous patient(e) dans une relation amoureuse ?", 14),
            
            # Attentes & style de vie
            ("Appréciez-vous les petites attentions romantiques ?", 15),
            ("Aimez-vous passer du temps de qualité à deux ?", 16),
            ("Êtes-vous à l'aise avec les démonstrations d'affection ?", 17),
            
            # Vision & avenir
            ("Vous projetez-vous facilement dans l'avenir avec la bonne personne ?", 18),
            ("Pensez-vous que l'amour peut rendre une personne meilleure ?", 19),
            ("Êtes-vous capable de faire des compromis dans une relation ?", 20),
        ]
        
        # Créer les questions
        for i, (text, order) in enumerate(questions_data, 1):
            Question.objects.create(text=text, order=order)
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {len(questions_data)} love relationship questions')
        )
