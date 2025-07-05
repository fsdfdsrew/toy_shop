#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Создаем директорию для медиа файлов если её нет
mkdir -p media

python manage.py collectstatic --no-input
python manage.py migrate 