# Student Matching Application

Une application web de matching entre étudiants basée sur un système de questions/réponses pour calculer la compatibilité.

## Fonctionnalités

- **Authentification utilisateur**: Inscription, connexion, déconnexion
- **Profil étudiant**: Photo, âge, filière, bio
- **Questionnaire**: 20 questions prédéfinies avec échelle 1-5
- **Algorithme de matching**: Calcul de compatibilité basé sur les réponses
- **Interface moderne**: Bootstrap 5, responsive design
- **Administration**: Interface Django admin pour gérer la plateforme

## Installation

1. Cloner le projet
2. Créer un environnement virtuel et l'activer
3. Installer les dépendances:
   ```bash
   pip install django pillow
   ```
4. Exécuter les migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. Créer les questions:
   ```bash
   python manage.py create_questions
   ```
6. Créer un superutilisateur:
   ```bash
   python manage.py createsuperuser
   ```
7. Démarrer le serveur:
   ```bash
   python manage.py runserver
   ```

## Structure du projet

- `accounts/`: Gestion de l'authentification
- `profiles/`: Profils étudiants avec photos
- `questions/`: Système de questions/réponses
- `matching/`: Algorithme de compatibilité et résultats
- `templates/`: Templates HTML avec Bootstrap
- `media/`: Fichiers uploadés (photos de profil)

## Utilisation

1. Créer un compte via le formulaire d'inscription
2. Compléter son profil avec photo et informations
3. Répondre au questionnaire de 20 questions
4. Découvrir les étudiants compatibles avec scores de compatibilité
5. Consulter les profils détaillés des matches

## Administration

Accéder à `/admin/` avec le compte superutilisateur pour:
- Gérer les utilisateurs
- Modifier les questions
- Superviser les réponses et matches

## Technologies

- **Backend**: Django 4.2.10 (Python)
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Base de données**: SQLite (développement)
- **Images**: Pillow pour le traitement des photos
