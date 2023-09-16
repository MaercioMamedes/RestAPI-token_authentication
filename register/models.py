from django.db import models

# Create your models here.


class Register(models.Model):
    name = models.CharField('name', max_length=100)
    username = models.CharField('username', max_length=50)
    phone = models.CharField('phone', max_length=11)
    email = models.EmailField('email')
    password = models.EmailField('password')

    def __str__(self):
        return self.name
