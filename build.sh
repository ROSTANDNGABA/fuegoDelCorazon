#!/bin/bash

# Script de build pour Render
echo "Installation des dépendances..."
pip install -r requirements.txt

echo "Création des fichiers statiques..."
python manage.py collectstatic --noinput

echo "Application des migrations de base de données..."
python manage.py migrate --noinput

echo "Vérification de la base de données..."
python manage.py showmigrations

echo "Build terminé avec succès!"
