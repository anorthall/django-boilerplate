#!/bin/bash

DB_URL_STR="${DATABASE_URL:-postgres://postgres:postgres@db:5432/postgres}"
DB_HOST="$(echo "$DB_URL_STR" | cut -d'@' -f2 | cut -d':' -f1)"
DB_PORT="$(echo "$DB_URL_STR" | cut -d'@' -f2 | cut -d':' -f2 | cut -d'/' -f1)"
export DJANGO_SETTINGS_MODULE="config.django.settings.${ENV_KIND}"

while ! nc -z "$DB_HOST" "$DB_PORT"; do
  sleep 0.1
done

if [ "$1" = "migrate" ]
then
    echo "Running migrations..."
    python src/manage.py migrate --no-input
fi

if [ "$1" = "test" ]
then
    echo "Running tests..."
    cd /app/src/ || exit 1
    pytest "${@:2}"
fi

if [ "$1" = "manage" ]
then
    cd /app/src/ || exit 1
    python manage.py "${@:2}"
fi

if [ "$1" = "devserver" ]
then
    echo "Collecting static files..."
    python src/manage.py collectstatic --noinput

    echo "Running migrations..."
    python src/manage.py migrate --no-input

    echo "Starting development server..."
    python src/manage.py runserver 0.0.0.0:"${PORT:=8000}" --insecure
fi

if [ "$1" = "worker" ]
then
    echo "Collecting static files..."
    python src/manage.py collectstatic --no-input

    echo "Starting worker..."
    celery -A config.django.celery worker -l info
fi

if [ "$1" = "start" ]
then
    echo "Installing TailwindCSS..."
    python src/manage.py tailwind install --no-input

    echo "Building TailwindCSS..."
    python src/manage.py tailwind build --no-input

    echo "Collecting static files..."
    python src/manage.py collectstatic --no-input

    if [ "$RUN_MIGRATIONS_ON_START" = "yes" ]
    then
        echo "Running migrations..."
        python src/manage.py migrate --no-input
    fi

    # Calculate gunicorn workers (CPU cores * 2 + 1)
    CPU_CORES=$(nproc --all)
    WORKERS=$((CPU_CORES * 2 + 1))
    echo "Detected $CPU_CORES CPU cores. Defaulting to $WORKERS gunicorn workers."

    echo "Starting server..."
    granian --interface wsgi --host 0.0.0.0 --port "${PORT:=8000}" --workers "$WORKERS" \
            --respawn-failed-workers --no-reload --no-ws config.django.wsgi:application
fi
