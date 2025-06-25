from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Escola, User

@admin.register(Escola)
class EscolaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cnpj', 'cidade', 'estado')
    search_fields = ('nome', 'cnpj')


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin): 
    model = User
    list_display = ('username', 'cpf', 'role', 'escola', 'is_active', 'is_staff')
    list_filter = ('role', 'escola', 'is_staff')
    search_fields = ('username', 'cpf', 'email')
    ordering = ('cpf',)

    fieldsets = (
        (None, {'fields': ('cpf', 'username', 'password')}),
        ('Informações pessoais', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissões', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Outros', {'fields': ('role', 'escola')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('cpf', 'username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'role', 'escola', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )

    def save_model(self, request, obj, form, change):
        raw_password = form.cleaned_data.get('password')
        if raw_password and not raw_password.startswith('pbkdf2_'):
            obj.set_password(raw_password)
        super().save_model(request, obj, form, change)
