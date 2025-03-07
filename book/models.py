from django.db import models
from datetime import date
import datetime
from django.utils import timezone
from django.db.models.base import Model
from users.models import Cadastro
# Create your models here.

# endereco

# biblioteca
class Biblioteca(models.Model):
    name_biblioteca = models.CharField(max_length=222)
    cep = models.IntegerField()
    rua = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name_biblioteca
    
# empresta
class Categorias(models.Model):
    nome = models.CharField(max_length=30)
    descricao = models.TextField()
    

    def __str__(self):
        return self.nome
    

# book
class Livros(models.Model):
    titulo = models.CharField(max_length=222)
    autor = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='fotos')
    descricao = models.TextField()
    emprestato = models.BooleanField(default=False)
    categoria = models.ForeignKey(Categorias, on_delete=models.DO_NOTHING)
    quantidade = models.IntegerField()
    data_cadastro = models.DateField(default= date.today)
    biblioteca = models.ForeignKey(Biblioteca, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = 'Livro'
    def __str__(self):
        return self.titulo
    
class Emprestimos(models.Model):
    choices = (
        ('P', 'Péssimo'),
        ('R', 'Ruim'),
        ('B','Bom'),
        ('O','Ótimo')
    )
    name_emprestado= models.ForeignKey(Cadastro, on_delete=models.DO_NOTHING, blank=True, null=True)
    data_emprestimo = models.DateTimeField(default=timezone.now)
    data_devolucao = models.DateTimeField(blank=True, null=True)
    livro = models.ForeignKey(Livros, on_delete=models.DO_NOTHING)
    avaliacao = models.CharField(max_length=1, choices=choices, null=True, blank=True)

    def __str__(self):
        return f'{self.name_emprestado} | {self.livro}'
