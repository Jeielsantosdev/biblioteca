from django.contrib.auth.backends import BaseBackend, ModelBackend
from django.contrib.auth.hashers import check_password
from .models import Cadastro # Substitua pelo seu modelo
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.http import Http404

class BackendDeAutenticacao(ModelBackend):
    def authenticate(self, request, user_email=None, password=None, **kwargs):
        user_model = get_user_model()
        try:
            user = get_object_or_404(user_model, user_email=user_email)
        except Http404:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None


    def get_user(self, id):
        try:
            return Cadastro.objects.get(id=id)
        except Cadastro.DoesNotExist:
            return None

# backend.py
from django.contrib.auth.backends import BaseBackend
from .models import Cadastro  # Ajuste para o caminho correto do seu modelo
'''
class EmailBackend(BaseBackend):
    def authenticate(self, request, user_email=None, password=None):
        try:
            user = Cadastro.objects.get(user_email=user_email)
            if user.check_password(password):
                return user
        except Cadastro.DoesNotExist:
            return None'
            '''

