from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.urls import path
from django.shortcuts import redirect
from django.utils.html import format_html
from .forms import UserCreationNoPasswordForm

from .models import Escola, User


# ============================
#  ESCOLA ADMIN
# ============================
@admin.register(Escola)
class EscolaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cnpj', 'cidade', 'estado')
    search_fields = ('nome', 'cnpj')
    ordering = ('nome',)


# ============================
#  USER ADMIN PERSONALIZADO
# ============================
@admin.register(User)
class CustomUserAdmin(DjangoUserAdmin):

    # CAMPOS NA LISTA
    add_form = UserCreationNoPasswordForm   
    form = UserCreationNoPasswordForm
    list_display = ("username", "cpf", "first_name", "last_name", "role", "escola", "is_active", "reset_password_button")
    list_filter = ("role", "escola", "is_staff")
    search_fields = ("username", "cpf", "first_name", "last_name", "email")
    ordering = ("cpf",)

    # CAMPOS AO EDITAR
    fieldsets = (
        (None, {"fields": ("cpf", "username", "password")}),
        ("Informações pessoais", {"fields": ("first_name", "last_name", "email")}),
        ("Permissões", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Outros", {"fields": ("role", "escola")}),
    )

    # CAMPOS AO CRIAR
    add_fieldsets = (
    (None, {
        "classes": ("wide",),
        "fields": ("cpf", "username", "first_name", "last_name", "email", "role", "escola"),
    }),
    )

    # 🔒 Impede edição do CPF após criado
    def get_readonly_fields(self, request, obj=None):
        if obj:  # se está editando
            return ("cpf", "password")
        return ("password",)  # ao criar, senha é gerada automaticamente

    # 🔽 Ordenar dropdown de escola
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "escola":
            kwargs["queryset"] = Escola.objects.order_by("nome")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # 🔐 Gera senha automática ao criar usuário
    def save_model(self, request, obj, form, change):
        if not change:
            obj.set_password("123456")
            obj.senha_temporaria = True
        super().save_model(request, obj, form, change)

    # ============================
    # BOTÃO RESETAR SENHA
    # ============================
    def reset_password_button(self, obj):
        return format_html(
            f'<a class="button" href="reset-password/{obj.id}">Resetar senha</a>'
        )
    reset_password_button.short_description = "Resetar senha"
    reset_password_button.allow_tags = True

    # URL extra para resetar senha
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("reset-password/<int:user_id>", self.admin_site.admin_view(self.reset_password_action), name="reset-user-password"),
        ]
        return custom_urls + urls

    # Ação de reset de senha
    def reset_password_action(self, request, user_id):
        user = User.objects.get(id=user_id)
        user.set_password("123456")
        user.senha_temporaria = True
        user.save()
        messages.success(request, f"A senha do usuário {user.username} foi resetada para 123456.")
        return redirect(f"/admin/home/user/{user_id}/change/")
