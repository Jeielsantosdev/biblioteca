from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Livros
from users.models import Cadastro
from django.contrib import messages
# Create your views here.
def livro(request,pk):
    livro = Livros.objects.filter(pk=pk)
    ...

def emprestimo(request, ):
    pass


def home(request):
    livros = Livros.objects.all()  # Busca todos os livros do BD
    context = {
        'livros': livros
    }
    return render(request, 'home.html', context)