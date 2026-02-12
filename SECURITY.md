# Sécurité pour Student Matching - Guide de déploiement

## 🔐 Configuration HTTPS et Sécurité

### 1. ALLOWED_HOSTS configuré ✅
- Ajout de `localhost` et `127.0.0.1` pour le développement
- Préparation pour les domaines de production
- Protection contre les attaques Host header

### 2. HTTPS prêt pour la production ✅
- Configuration SSL/TLS complète
- Headers de sécurité activés
- Cookies sécurisés pour HTTPS

## 📋 Étapes de déploiement sécurisé

### Étape 1: Variables d'environnement
```bash
# Copier le fichier d'exemple
cp .env.example .env

# Éditer avec vos vraies valeurs
nano .env
```

### Étape 2: Configuration de production
```bash
# Utiliser les settings de production
export DJANGO_SETTINGS_MODULE=student_matching.settings_production
```

### Étape 3: Base de données PostgreSQL
```bash
# Installer PostgreSQL
sudo apt update
sudo apt install postgresql postgresql-contrib

# Créer la base de données
sudo -u postgres createdb student_matching
sudo -u postgres createuser --interactive
```

### Étape 4: Installation SSL avec Let's Encrypt
```bash
# Installer Certbot
sudo apt install certbot python3-certbot-nginx

# Obtenir un certificat SSL gratuit
sudo certbot --nginx -d votredomaine.com -d www.votredomaine.com
```

### Étape 5: Déploiement avec le script
```bash
# Rendre le script exécutable
chmod +x deploy.sh

# Exécuter le déploiement
sudo ./deploy.sh
```

## 🛡️ Mesures de sécurité activées

### ✅ Headers de sécurité
- **HSTS**: Force HTTPS pendant 1 an
- **X-Frame-Options**: Empêche le clickjacking
- **X-Content-Type-Options**: Empêche le MIME-sniffing
- **X-XSS-Protection**: Protection contre XSS

### ✅ Cookies sécurisés
- **Secure**: Uniquement sur HTTPS
- **HttpOnly**: Inaccessibles via JavaScript
- **SameSite**: Protection CSRF

### ✅ Configuration SSL
- **TLS 1.2/1.3**: Protocoles modernes
- **Ciphers forts**: Chiffrement robuste
- **Redirection automatique**: HTTP → HTTPS

## 🚀 Commandes utiles

### Vérification de la sécurité
```bash
# Test des headers de sécurité
curl -I https://votredomaine.com

# Vérification SSL
openssl s_client -connect votredomaine.com:443

# Test de configuration Django
python manage.py check --deploy
```

### Monitoring
```bash
# Logs Gunicorn
journalctl -u gunicorn -f

# Logs Nginx
tail -f /var/log/nginx/access.log

# Statut des services
systemctl status gunicorn nginx
```

## ⚠️ Points critiques à vérifier

1. **SECRET_KEY**: Générer une nouvelle clé pour la production
2. **ALLOWED_HOSTS**: Ajouter votre vrai domaine
3. **Base de données**: Utiliser PostgreSQL au lieu de SQLite
4. **HTTPS**: Activer tous les paramètres SSL en production
5. **Firewall**: Configurer ufw pour n'autoriser que 80, 443, 22

## 🎯 Résultat final

Votre application sera maintenant:
- 🔐 **Sécurisée** avec HTTPS et headers de protection
- 🚀 **Performante** avec Nginx + Gunicorn
- 📊 **Monitored** avec logs et monitoring
- 🔄 **Maintenable** avec scripts de déploiement automatiques

**Les mots de passe circuleront maintenant de manière sécurisée!** 🛡️
