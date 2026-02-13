DEPLOYMENT GUIDE — Student Matching

Résumé rapide
- Destiné à un déploiement sur Render (ex. https://render.com).
- Actions essentielles : définir `SECRET_KEY`, mettre `DEBUG=False`, configurer `ALLOWED_HOSTS`, exécuter migrations et `collectstatic`.

Étapes (Render dashboard)
1. Dans le service Web > Environment > Environment Variables, ajouter :
   - `SECRET_KEY` = "<votre_cle_secrete_prod>"
   - `DEBUG` = `False`
   - `ALLOWED_HOSTS` = `fuegodelcorazon-1.onrender.com`  # ou votre domaine
   - Optionnel : `DATABASE_URL` si vous utilisez PostgreSQL

2. Deploy environment :
   - Build command : `pip install -r requirements.txt`
   - Start command : `gunicorn student_matching.wsgi`

3. Après déploiement, exécuter (Render > Shell ou via web console) :
```bash
# exécuter dans le dossier du projet sur l'instance
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

4. Vérifications post‑déploiement
- Ouvrir l'URL publique et se connecter à `/admin/`.
- Créer un compte test, créer/modifier un profil, répondre au questionnaire, vérifier les matches.
- Vérifier les logs Render pour erreurs.

Conseils de sécurité
- Ne jamais committer `SECRET_KEY` dans le dépôt.
- Mettre `DEBUG=False` en production.
- Utiliser HTTPS et configurer les headers de sécurité (HSTS, cookies_secure).

Debug local
- Pour dev local, exportez temporairement la clé :
```powershell
$env:SECRET_KEY='dev-secret-key-local'
python manage.py runserver
```

Annexe — commandes utiles
```bash
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
```

Questions ? Demandez si vous voulez que je crée une PR avec ce fichier ou que je génère un script `deploy.sh`.