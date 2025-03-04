from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _

# Create your models here.

class UsuarioManager(BaseUserManager):
    def create_user(self, user_email, username, password=None, **extra_fields):
        if not user_email:
            raise ValueError("O campo email é obrigatório")
        email = self.normalize_email(user_email)
        user = self.model(user_email=user_email, username=username, **extra_fields)
        user.set_password(password)  # Usa o método seguro do Django
        user.save(using=self._db)
        return user

    def create_superuser(self, user_email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(user_email, username, password, **extra_fields)


class Cadastro(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100)
    user_email = models.EmailField(unique=True)
    date_birth = models.DateField(null=True)
    foto = models.ImageField(upload_to='fotos')
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(default=now, blank=True, null=True) 


    groups = models.ManyToManyField(
        "auth.Group",
        related_name="cadastro_users",  # Nome único para evitar conflito
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="cadastro_users_permissions",  # Nome único para evitar conflito
        blank=True
    )


    objects = UsuarioManager()

    USERNAME_FIELD = 'user_email'
    
    
    def __str__(self):
        return f'{self.username} | {self.user_email}'
