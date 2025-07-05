#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Создаем директорию для медиа файлов если её нет
mkdir -p media
mkdir -p staticfiles/media

# Копируем медиа файлы в staticfiles
cp -r media/* staticfiles/media/

python manage.py collectstatic --no-input
python manage.py migrate 