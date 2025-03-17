from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Cadastro

class CadastroAdmin(UserAdmin):
    model = Cadastro
    list_display = ('user_email', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'date_birth')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('user_email',)
    ordering = ('user_email',)

    fieldsets = (
        (None, {'fields': ('user_email', 'password')}),
        ('Informações Pessoais', {'fields': ('date_birth', 'foto')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_email', 'password', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )

admin.site.register(Cadastro, CadastroAdmin)
