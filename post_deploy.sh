#!/usr/bin/env bash
set -euo pipefail

echo "Running post-deploy tasks..."

echo "1) Apply migrations"
python manage.py migrate

echo "2) Collect static files"
python manage.py collectstatic --noinput

echo "Post-deploy tasks completed."
