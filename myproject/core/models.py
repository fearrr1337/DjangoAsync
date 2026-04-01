from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('guest', 'Гость'),
        ('user','Пользователь'),
        ('moderator','Модератор'),
        ('admin','Администратор'),
    )
    role = models.CharField(max_length=20,choices=ROLE_CHOICES, default='user')

    phone = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(max_length=20, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        permissions = [
            ('can_moderate', "Может модерировать"),
            ('can_manage_users', "Может управлять пользователями")
        ]