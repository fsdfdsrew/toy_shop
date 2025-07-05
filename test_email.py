#!/usr/bin/env python
"""
Тестовый скрипт для проверки отправки писем
Запускайте только после настройки SMTP в settings.py
"""

import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'toy_shop.settings')
django.setup()

from toys.models import Order, Toy, OrderItem
from toys.tasks import send_order_confirmation_email

def test_email_sending():
    """Тестирует отправку писем"""
    
    # Проверяем, есть ли игрушки в базе
    toys = Toy.objects.filter(is_active=True)
    if not toys.exists():
        print("❌ Ошибка: В базе данных нет активных игрушек")
        print("Добавьте игрушки через админку Django или создайте их программно")
        return
    
    # Берем первую доступную игрушку
    toy = toys.first()
    print(f"Используем игрушку: {toy.name}")
    
    # Создаем тестовый заказ
    order = Order.objects.create(
        first_name="Иван",
        last_name="Иванов",
        email="test@example.com",  # Измените на реальный email для тестирования
        phone="+7 (999) 123-45-67",
        address="г. Москва, ул. Тестовая, д. 1, кв. 1",
        total_amount=toy.price * 2
    )
    
    # Создаем товар заказа
    OrderItem.objects.create(
        order=order,
        toy=toy,
        quantity=2,
        price=toy.price,
        subtotal=toy.price * 2
    )
    
    print(f"Создан тестовый заказ #{order.order_number}")
    
    print("Тестирование отправки письма клиенту...")
    try:
        result = send_order_confirmation_email.delay(order.id)
        print(f"Задача отправлена. ID задачи: {result.id}")
        print("Проверьте email клиента")
    except Exception as e:
        print(f"Ошибка при отправке письма клиенту: {e}")

if __name__ == "__main__":
    print("=== Тестирование отправки писем ===")
    print("Убедитесь, что:")
    print("1. Настроены SMTP параметры в settings.py")
    print("2. RabbitMQ запущен")
    print("3. Celery worker запущен в отдельном терминале")
    print("4. В базе данных есть игрушки")
    print()
    
    input("Нажмите Enter для продолжения...")
    
    test_email_sending()
    
    print("\n=== Тестирование завершено ===")
    print("Для просмотра результатов проверьте:")
    print("- Email клиента")
    print("- Логи Celery worker") 