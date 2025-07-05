@echo off
echo ========================================
echo Запуск сервисов магазина игрушек
echo ========================================
echo.

echo 1. Проверка RabbitMQ...
echo Убедитесь, что RabbitMQ запущен как служба Windows
echo.

echo 2. Запуск Django сервера...
echo Откройте новый терминал и выполните:
echo python manage.py runserver
echo.

echo 3. Запуск Celery worker...
echo Откройте новый терминал и выполните:
echo celery -A toy_shop worker --loglevel=info
echo.

echo 4. Настройка email (обязательно!)
echo Отредактируйте toy_shop/settings.py:
echo - EMAIL_HOST_USER
echo - EMAIL_HOST_PASSWORD  
echo - DEFAULT_FROM_EMAIL
echo - ADMIN_EMAIL
echo.

echo 5. Тестирование
echo Запустите: python test_email.py
echo.

pause 