from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import Cadastro # Substitua pelo seu modelo

class BackendDeAutenticacao(BaseBackend):
    def authenticate(self, request, user_email=None, senha=None):
        try:
            user = Cadastro.objects.get(user_email=user_email)
            if check_password(senha, user.senha):  # Verifica a senha
                return user
        except Cadastro.DoesNotExist:
            return None
        return None

    def get_user(self, id):
        try:
            return Cadastro.objects.get(id=id)
        except Cadastro.DoesNotExist:
            return None
