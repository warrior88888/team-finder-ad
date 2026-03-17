#!/bin/bash
set -e

# Fix permissions on mounted volumes at runtime
# (Docker volumes override build-time chown, so we do it here as root)
chown -R django:django /app/media /app/collected_static /var/log/django

echo "--> Collecting static files..."
gosu django python manage.py collectstatic --noinput -v 0

echo "--> Applying database migrations..."
gosu django python manage.py migrate --noinput

echo "--> Starting Gunicorn..."
exec gosu django "$@"