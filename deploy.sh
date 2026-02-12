#!/bin/bash

# Script de déploiement sécurisé pour Student Matching
# Usage: ./deploy.sh

echo "🚀 Déploiement de Student Matching en production..."

# Vérifications
if [ "$EUID" -ne 0 ]; then
    echo "❌ Ce script doit être exécuté en tant que root (sudo)"
    exit 1
fi

# Variables (à adapter)
PROJECT_DIR="/var/www/student_matching"
VENV_DIR="$PROJECT_DIR/venv"
DOMAIN="votredomaine.com"
EMAIL="admin@votredomaine.com"

echo "📁 Mise à jour du code..."
cd $PROJECT_DIR
git pull origin main

echo "🐍 Activation de l'environnement virtuel..."
source $VENV_DIR/bin/activate

echo "📦 Installation des dépendances..."
pip install -r requirements.txt

echo "🗄️ Migration de la base de données..."
python manage.py migrate --settings=student_matching.settings_production

echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput --settings=student_matching.settings_production

echo "🔍 Vérification de la configuration Django..."
python manage.py check --deploy --settings=student_matching.settings_production

echo "🔄 Redémarrage de Gunicorn..."
systemctl restart gunicorn
systemctl enable gunicorn

echo "🌐 Rechargement de Nginx..."
nginx -t && systemctl reload nginx

echo "🔐 Installation du certificat SSL avec Let's Encrypt..."
if [ ! -f "/etc/letsencrypt/live/$DOMAIN/fullchain.pem" ]; then
    certbot --nginx -d $DOMAIN -d www.$DOMAIN --email $EMAIL --agree-tos --non-interactive
else
    certbot renew --quiet
fi

echo "✅ Vérification du service..."
systemctl status gunicorn --no-pager
systemctl status nginx --no-pager

echo "🎉 Déploiement terminé!"
echo "🌐 Votre site est disponible sur: https://$DOMAIN"
echo "📊 Logs: journalctl -u gunicorn -f"
