from django.apps import AppConfig
from django.contrib import admin
from register.models import Register


class RegisterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    verbose_name = 'General register'
    name = 'register'


class RegisterAdmin(admin.ModelAdmin):
    pass


admin.site.register(Register, RegisterAdmin)
