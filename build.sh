#!/bin/bash

# Script de build pour Render
echo "=== Début du build pour Render ==="

echo "1. Installation des dépendances..."
pip install -r requirements.txt

echo "2. Création des fichiers statiques..."
python manage.py collectstatic --noinput --clear

echo "3. Application des migrations de base de données..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "4. Vérification de la base de données..."
python manage.py showmigrations

echo "5. Création d'un superutilisateur si nécessaire..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123')" | python manage.py shell

echo "=== Build terminé avec succès! ==="
