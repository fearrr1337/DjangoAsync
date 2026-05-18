import logging
import time
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)
User = get_user_model()

# Старая задача, оставлена для совместимости
@shared_task
def add(x, y):
    time.sleep(5)
    return x + y

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_welcome_email(self, user_id):
    """Отправляет приветственное письмо новому пользователю."""
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        logger.error(f"Пользователь с id={user_id} не найден")
        return

    subject = "Добро пожаловать!"
    message = render_to_string('core/emails/welcome.html', {'user': user})
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        logger.info(f"Приветственное письмо отправлено пользователю {user.username}")
    except Exception as exc:
        logger.warning(f"Ошибка отправки приветственного письма: {exc}")
        raise self.retry(exc=exc)

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_password_reset_email(self, user_id, reset_url):
    """Асинхронная отправка письма для сброса пароля."""
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        logger.error(f"Пользователь с id={user_id} не найден")
        return

    subject = "Сброс пароля"
    message = render_to_string('core/emails/password_reset.html', {
        'user': user,
        'reset_url': reset_url
    })
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        logger.info(f"Письмо сброса пароля отправлено {user.username}")
    except Exception as exc:
        logger.warning(f"Ошибка отправки письма сброса: {exc}")
        raise self.retry(exc=exc)

@shared_task
def delete_inactive_users():
    """
    Периодическая задача: удаляет пользователей,
    которые не активировали аккаунт в течение 7 дней.
    """
    from datetime import timedelta
    from django.utils import timezone

    threshold = timezone.now() - timedelta(days=7)
    inactive_users = User.objects.filter(
        is_active=False,
        date_joined__lt=threshold
    )
    count = inactive_users.count()
    inactive_users.delete()
    logger.info(f"Удалено {count} неактивированных пользователей")
    return count