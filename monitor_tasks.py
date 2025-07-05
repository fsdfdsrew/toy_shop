#!/usr/bin/env python
"""
Скрипт для мониторинга задач Celery
"""

import os
import django
import time

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'toy_shop.settings')
django.setup()

from django_celery_results.models import TaskResult

def monitor_tasks():
    """Мониторинг выполненных задач"""
    print("=== Мониторинг задач Celery ===")
    
    # Получаем последние 10 задач
    tasks = TaskResult.objects.all().order_by('-date_done')[:10]
    
    if not tasks:
        print("Нет выполненных задач")
        return
    
    print(f"Последние {len(tasks)} задач:")
    print("-" * 80)
    
    for task in tasks:
        status = "✅ УСПЕШНО" if task.status == "SUCCESS" else f"❌ {task.status}"
        print(f"ID: {task.task_id}")
        print(f"Задача: {task.task_name}")
        print(f"Статус: {status}")
        print(f"Время выполнения: {task.date_done}")
        if task.result:
            print(f"Результат: {task.result}")
        print("-" * 80)

def monitor_active_tasks():
    """Мониторинг активных задач"""
    print("=== Активные задачи ===")
    
    try:
        from celery import current_app
        inspect = current_app.control.inspect()
        active = inspect.active()
        
        if not active:
            print("Нет активных задач")
            return
        
        for worker, tasks in active.items():
            print(f"Worker: {worker}")
            for task in tasks:
                print(f"  - {task['name']} (ID: {task['id']})")
                print(f"    Время начала: {task['time_start']}")
                print(f"    Аргументы: {task['args']}")
    except Exception as e:
        print(f"Ошибка при получении активных задач: {e}")

if __name__ == "__main__":
    while True:
        print("\n" + "="*50)
        monitor_tasks()
        print()
        monitor_active_tasks()
        print("\nОбновление через 5 секунд... (Ctrl+C для выхода)")
        time.sleep(5) 