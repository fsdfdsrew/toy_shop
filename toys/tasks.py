from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Order


@shared_task
def send_order_confirmation_email(order_id):
    """
    Отправляет письмо с подтверждением заказа
    """
    try:
        order = Order.objects.get(id=order_id)
        
        # Подготавливаем данные для письма
        context = {
            'order': order,
            'items': order.items.all(),
        }
        
        # Рендерим HTML и текстовую версии письма
        html_message = render_to_string('toys/emails/order_confirmation.html', context)
        text_message = render_to_string('toys/emails/order_confirmation.txt', context)
        
        # Отправляем письмо
        send_mail(
            subject=f'Подтверждение заказа #{order.order_number}',
            message=text_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        print(f"Письмо с подтверждением заказа #{order.order_number} отправлено на {order.email}")
        return True
        
    except Order.DoesNotExist:
        print(f"Заказ с ID {order_id} не найден")
        return False
    except Exception as e:
        print(f"Ошибка при отправке письма: {e}")
        return False 