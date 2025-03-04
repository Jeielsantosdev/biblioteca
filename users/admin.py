from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from .models import Cadastro

# Personalizando o CadastroAdmin sem usar forms
class CadastroAdmin(UserAdmin):
    model = Cadastro
    # Campos que serão exibidos no painel do Admin
    list_display = ('user_email', 'username', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'date_birth')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('user_email', 'username')
    ordering = ('user_email',)
    
    # Campos para a visualização do formulário de criação e alteração
    fieldsets = (
        (None, {'fields': ('user_email', 'password')}),
        ('Informações Pessoais', {'fields': ('username', 'date_birth', 'foto')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas', {'fields': ('last_login',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_email', 'username', 'password', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )

    # Usando o PasswordInput diretamente no admin
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'password':
            from django.forms import PasswordInput
            kwargs['widget'] = PasswordInput()
        return super().formfield_for_dbfield(db_field, request, **kwargs)

    # Para criar um superusuário através do Admin
    def save_model(self, request, obj, form, change):
        if not obj.pk and not obj.is_staff:
            obj.is_staff = True  # Garantir que superusuários tenham permissões para o admin
        super().save_model(request, obj, form, change)

admin.site.register(Cadastro, CadastroAdmin)

