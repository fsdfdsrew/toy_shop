# Магазин игрушек с асинхронной рассылкой писем

## Описание

Веб-приложение магазина игрушек на Django с асинхронной рассылкой писем с помощью Celery и RabbitMQ.

## Функциональность

- Каталог игрушек с фильтрацией и поиском
- Корзина покупок
- Оформление заказов
- **Асинхронная рассылка писем** при оформлении заказа:
  - Письмо с подтверждением заказа клиенту

## Установка и настройка

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Настройка базы данных

```bash
python manage.py migrate
```

### 3. Настройка RabbitMQ

Установите и запустите RabbitMQ:

**Windows:**

- Скачайте и установите [RabbitMQ](https://www.rabbitmq.com/download.html)
- Запустите службу RabbitMQ

**Linux/macOS:**

```bash
# Ubuntu/Debian
sudo apt-get install rabbitmq-server
sudo systemctl start rabbitmq-server

# macOS
brew install rabbitmq
brew services start rabbitmq
```

### 4. Настройка email

Отредактируйте `toy_shop/settings.py`:

```python
# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Ваш SMTP сервер
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'  # Ваш email
EMAIL_HOST_PASSWORD = 'your-app-password'  # Пароль приложения
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'  # Ваш email
```

### 5. Запуск приложения

#### Терминал 1: Django сервер

```bash
python manage.py runserver
```

#### Терминал 2: Celery worker

```bash
celery -A toy_shop worker --loglevel=info --pool=solo
```

#### Терминал 3: Celery beat (опционально, для периодических задач)

```bash
celery -A toy_shop beat --loglevel=info
```

## Как это работает

1. Пользователь оформляет заказ на сайте
2. Заказ сохраняется в базе данных
3. Пользователь перенаправляется на страницу успешного оформления
4. **Асинхронно** отправляется письмо клиенту с подтверждением заказа

## Структура проекта

```
toy_shop/
├── toy_shop/
│   ├── celery.py          # Конфигурация Celery
│   ├── settings.py        # Настройки Django
│   └── __init__.py        # Импорт Celery
├── toys/
│   ├── tasks.py           # Задачи Celery для отправки писем
│   ├── views.py           # Views Django
│   ├── models.py          # Модели данных
│   └── templates/
│       └── toys/
│           └── emails/    # Шаблоны писем
├── requirements.txt       # Зависимости
└── README.md             # Документация
```

## Шаблоны писем

- `order_confirmation.html/.txt` - Письмо клиенту с подтверждением заказа

## Мониторинг задач

Для мониторинга выполнения задач Celery используйте:

```bash
# Просмотр активных задач
celery -A toy_shop inspect active

# Просмотр статистики
celery -A toy_shop inspect stats

# Мониторинг через скрипт
python monitor_tasks.py
```

## Примечания

- Убедитесь, что RabbitMQ запущен перед запуском Celery worker
- Для продакшена рекомендуется использовать Redis вместо django-db для результатов
- Настройте правильные SMTP параметры для отправки писем
