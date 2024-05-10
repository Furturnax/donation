import os

from celery import shared_task
from django.core.mail import send_mail
from dotenv import load_dotenv

from collect.models import Payment, Collect

load_dotenv(
    dotenv_path='./docker/envfiles/.env'
)


@shared_task
def send_payment_created_email(payment_id):
    payment = Payment.objects.get(pk=payment_id)
    subject = f'Donation. Информация о платяже № {payment_id}.'
    message = (
        f'Приветствуем тебя, {payment.user.first_name}. Платеж к сбору '
        f'{payment.collect.title} успешно создан! '
        f'Уникальный номер {payment_id}.'
    )
    sender = os.getenv('EMAIL_HOST_USER')
    recipient_list = [payment.user.email]
    return send_mail(
        subject, message, sender, recipient_list, fail_silently=True
    )


@shared_task
def send_collect_created_email(collect_id):
    collect = Collect.objects.get(pk=collect_id)
    subject = f'Donation. Информация о сборе № {collect_id}.'
    message = (
        f'Приветствуем тебя, {collect.author.first_name}. Сбор '
        f'{collect.title} успешно создан! '
        f'Уникальный номер {collect_id}.'
    )
    sender = os.getenv('EMAIL_HOST_USER')
    recipient_list = [collect.author.email]
    return send_mail(
        subject, message, sender, recipient_list, fail_silently=True
    )
