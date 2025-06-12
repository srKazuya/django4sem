from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_test_email():
    send_mail(
        subject='Проверка Celery',
        message='Это тестовая рассылка по расписанию.',
        from_email='from@example.com',
        recipient_list=['test@example.com'],
    )

@shared_task
def send_order_confirmation_email(email: str, order_id: int, total_price: float) -> None:
    """
    Отправляет письмо с подтверждением заказа.

    :param email: Email пользователя
    :param order_id: ID заказа
    :param total_price: Сумма заказа
    """
    subject = f'Подтверждение заказа #{order_id}'
    message = f'Спасибо за ваш заказ!\nНомер заказа: {order_id}\nСумма: {total_price} руб.'
    send_mail(
        subject,
        message,
        'noreply@example.com', 
        [email],
    )