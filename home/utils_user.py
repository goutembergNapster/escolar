
from django.contrib.auth import get_user_model

User = get_user_model()

def criar_usuario_com_cpf(cpf, senha, role, escola=None, email=None, is_staff=False, is_superuser=False):
    if User.objects.filter(cpf=cpf).exists():
        return User.objects.get(cpf=cpf)  # evita duplicidade

    user = User.objects.create_user(
        username=cpf,
        cpf=cpf,
        password=senha,
        role=role,
        escola=escola,
        email=email or '',
    )

    user.is_active = True
    user.is_staff = is_staff
    user.is_superuser = is_superuser
    user.save()

    return user