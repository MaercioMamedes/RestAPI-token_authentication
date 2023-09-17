from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Register(models.Model):
    fullname = models.CharField('name', max_length=100)
    phone = models.CharField('phone', max_length=11)
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1, null=False, blank=False)

    def __str__(self):
        return self.user.first_name
