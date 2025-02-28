from django.db import models
from django.utils.timezone import now
# Create your models here.


class Cadastro(models.Model):
    username = models.CharField(max_length=100)
    user_email = models.EmailField(unique=True)
    date_birth = models.DateField(null=True)
    senha = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='fotos')
    is_active = models.BooleanField(default=False)
    last_login = models.DateTimeField(default=now, blank=True, null=True) 

    def __str__(self):
        return f'{self.username} | {self.user_email}'
