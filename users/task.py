from django.core.mail import send_mail
from time import sleep

from celery import shared_task


@shared_task()
def send_email(email):
    sleep(5)
    send_mail(
        'Registration',
        'You successfully registered on courses site app.',
        'lkjhgfdsa@fastmail.com',
        [email]
    )
