from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    first_name = models.CharField(max_length=255, default='Имя', verbose_name='Имя')
    last_name = models.CharField(max_length=255, default='Фамилия',  verbose_name='Фамилия')
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
