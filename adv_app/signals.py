from django.shortcuts import render, reverse, redirect
from django.dispatch import receiver
from django.core.mail import send_mail, mail_managers
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.template.loader import render_to_string

from .models import Adv, Reply
from django.contrib.auth.models import User

# Приветственное письмо и письмо об изменении данных
@receiver(post_save, sender=User)
def hello_user(sender, instance, created, **kwargs):
    if created:
        username = instance.username
        email = instance.email
        message = (f'{instance.username}, добро пожаловать на наш портал! '
                   f'В следующем письме вам придет код подтверждения, '
                   f'пожалуйста, завершите регистрацию и можете приступать к созданию своего первого объявления!'
                   )
        send_mail(
            subject=f'Личная информация',
            message=message,
            from_email='marinaprosche@yandex.ru',
            recipient_list=[email],
        )