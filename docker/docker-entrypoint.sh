#!/bin/sh
set -e

# app specific setup here
python manage.py migrate
python manage.py remove_stale_contenttypes --include-stale-apps --noinput

mkdir -p /app/static
chown $MEDIA_FOLDER_UID:$MEDIA_FOLDER_GID /app/static
# collect static if needed
python manage.py collectstatic --noinput

export GIT_COMMIT=$(git rev-parse HEAD)
export GIT_COMMIT_SHORT=$(git rev-parse --short HEAD)
export GIT_BRANCH=$(git branch --show-current)
export GIT_TAG=$(git tag --points-at HEAD | head -n 1)

# fix media folder permissions for nginx
MEDIA_FOLDER_UID=${MEDIA_FOLDER_UID-101}
MEDIA_FOLDER_GID=${MEDIA_FOLDER_GID-101}
mkdir -p /media/images /media/thumbnails
chown $MEDIA_FOLDER_UID:$MEDIA_FOLDER_GID /media /media/images /media/thumbnails
mkdir -p /static-vite/dist/assets
chown $MEDIA_FOLDER_UID:$MEDIA_FOLDER_GID /static-vite/dist /static-vite/dist/assets

# ensure django file cache directory exists
mkdir -p /django_cache

gunicorn --config /app/gunicorn.config.py digital_mary_app.wsgi:application