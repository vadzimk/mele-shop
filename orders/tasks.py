from django.conf import settings
from celery import shared_task
from django.core.mail import send_mail

from orders.models import Order
from . import logger


@shared_task
def order_created(order_id):
    """ send email notification when order created """
    email_from = settings.EMAIL_FROM
    order = Order.objects.get(id=order_id)
    subject = f'Order #{order.id}'
    message = f"""Dear {order.first_name},
    Your order have been placed
    Order id is {order.id}"""
    mail_sent = send_mail(subject,
                          message,
                          email_from,
                          [order.email],
                          fail_silently=False, )
    logger.info(f'sending email from {email_from} to {order.email} result: {mail_sent}')
    return mail_sent
