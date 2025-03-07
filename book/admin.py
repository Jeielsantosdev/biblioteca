from django.contrib import admin
from .models import Biblioteca, Livros, Emprestimos,Categorias
# Register your models here.


admin.site.register(Livros)
admin.site.register(Biblioteca)
admin.site.register(Emprestimos)
admin.site.register(Categorias)
