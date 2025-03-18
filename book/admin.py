from django.contrib import admin
from .models import Biblioteca, Livros, Emprestimos,Categorias
# Register your models here.


# Administração de Livros
class LivrosAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'categoria', 'quantidade', 'emprestado', 'biblioteca')
    list_filter = ('categoria', 'emprestado')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(biblioteca__usuario_admin=request.user)

    def has_add_permission(self, request):
        return request.user.is_superuser or Biblioteca.objects.filter(usuario_admin=request.user).exists()

    def has_change_permission(self, request, obj=None):
        if obj and obj.biblioteca.usuario_admin != request.user:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        if obj and obj.biblioteca.usuario_admin != request.user:
            return False
        return True

# Administração de Empréstimos
class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ('name_emprestado', 'livro', 'data_emprestimo', 'data_devolucao', 'avaliacao')
    list_filter = ('data_emprestimo', 'avaliacao')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(livro__biblioteca__usuario_admin=request.user)

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

admin.site.register(Livros, LivrosAdmin)
admin.site.register(Biblioteca)
admin.site.register(Emprestimos, EmprestimoAdmin)
admin.site.register(Categorias)
